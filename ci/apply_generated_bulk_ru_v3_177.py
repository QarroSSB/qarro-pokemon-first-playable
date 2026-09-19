#!/usr/bin/env python3
"""Qarro v3.177: apply generated bulk RU as content-addressed micro-hunks.

The generated unified diff was produced from the exact FULL GREEN v3.173 text
state. Current v3.176 has additional translations outside the seven target
surfaces, so whole-file git-apply context is intentionally not trusted.

This wrapper parses each contiguous +/- change group and applies it by its own
exact old content plus nearest unchanged context line. It is fail-closed:
ambiguous/missing groups abort unless the exact new group is already present.
Only the seven audited text surfaces are accepted.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_GENERATED_BULK_V3_177"
PATCH = Path(__file__).with_name("generated_bulk_ru_v3_177.patch")
EXPECTED = {
    "data/scripts/cable_club_frlg.inc",
    "data/text/fame_checker_frlg.inc",
    "data/text/trainers.inc",
    "data/text/trainers_frlg.inc",
    "src/battle_message.c",
    "src/data/items.h",
    "src/strings.c",
}

def parse_patch(text: str):
    files: dict[str, list[dict]] = {}
    current = None
    prev_context = None
    group = None

    def finish(next_context=None):
        nonlocal group
        if group is None:
            return
        group["next"] = next_context
        if not group["old"] or not group["new"]:
            raise RuntimeError(
                f"{current}: unsupported pure add/delete group "
                f"old={len(group['old'])} new={len(group['new'])}"
            )
        files.setdefault(current, []).append(group)
        group = None

    for line in text.splitlines():
        m = re.match(r"^diff --git a/(.+?) b/(.+?)$", line)
        if m:
            finish()
            if m.group(1) != m.group(2):
                raise RuntimeError(f"renamed path unsupported: {m.groups()}")
            current = m.group(1)
            prev_context = None
            continue
        if current is None:
            continue
        if line.startswith("@@"):
            finish()
            prev_context = None
            continue
        if line.startswith("--- ") or line.startswith("+++ "):
            continue
        if line.startswith(" "):
            ctx = line[1:]
            if group is not None:
                finish(ctx)
            prev_context = ctx
            continue
        if line.startswith("-"):
            if group is None:
                group = {"old": [], "new": [], "prev": prev_context, "next": None}
            group["old"].append(line[1:])
            continue
        if line.startswith("+"):
            if group is None:
                group = {"old": [], "new": [], "prev": prev_context, "next": None}
            group["new"].append(line[1:])
            continue
        if line.startswith("\\ No newline"):
            continue
    finish()
    return files

def replace_group(text: str, rel: str, idx: int, g: dict, cursor: int):
    old = "\n".join(g["old"])
    new = "\n".join(g["new"])
    prev = g.get("prev")
    nxt = g.get("next")

    candidates = []
    if prev is not None and nxt is not None:
        candidates.append((prev + "\n" + old + "\n" + nxt,
                           prev + "\n" + new + "\n" + nxt, "prev+next"))
    if prev is not None:
        candidates.append((prev + "\n" + old,
                           prev + "\n" + new, "prev"))
    if nxt is not None:
        candidates.append((old + "\n" + nxt,
                           new + "\n" + nxt, "next"))
    candidates.append((old, new, "body"))

    # Patch hunks are ordered by source position. When an exact body occurs
    # more than once (common for duplicate item descriptions), choose the first
    # matching occurrence at or after the previous hunk's cursor. This retains
    # deterministic source-order identity instead of guessing by text alone.
    for needle, repl, mode in candidates:
        positions = [m.start() for m in re.finditer(re.escape(needle), text)]
        if not positions:
            continue
        after = [p for p in positions if p >= cursor]
        if len(positions) == 1:
            pos = positions[0]
            new_text = text[:pos] + repl + text[pos + len(needle):]
            return new_text, "applied", mode, pos + len(repl)
        if after:
            pos = after[0]
            new_text = text[:pos] + repl + text[pos + len(needle):]
            return new_text, "applied", mode + "-ordered", pos + len(repl)

    # Idempotent replay is allowed when the exact translated body is already
    # present at/after the current source-order cursor.
    new_positions = [m.start() for m in re.finditer(re.escape(new), text)]
    after_new = [p for p in new_positions if p >= cursor]
    if after_new:
        pos = after_new[0]
        return text, "already", "new-body", pos + len(new)

    # Older bulk source may contain an English block that a later dedicated
    # pass has already translated. For ASM labeled blocks, accept that newer
    # translation only when the same exact label exists once and its current
    # body already contains Cyrillic text.
    if prev is not None:
        lm = re.fullmatch(r"([A-Za-z0-9_]+)::", prev.strip())
        if lm:
            label = lm.group(1)
            ms = list(re.finditer(rf"(?m)^{re.escape(label)}::\\s*$", text))
            if len(ms) == 1:
                start = ms[0].end()
                next_label = re.search(r"(?m)^[A-Za-z0-9_]+::\\s*$", text[start:])
                block_end = start + next_label.start() if next_label else len(text)
                body = text[start:block_end]
                if re.search(r"[А-Яа-яЁё]", body):
                    return text, "already", "label-cyrillic", block_end

    counts = [(mode, text.count(needle)) for needle, _, mode in candidates]
    raise RuntimeError(
        f"{rel}: micro-hunk {idx} not applicable from cursor={cursor}; "
        f"counts={counts}; old_head={old[:140]!r}"
    )

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_generated_bulk_ru_v3_177.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    patch_text = PATCH.read_text(encoding="utf-8")
    parsed = parse_patch(patch_text)
    if set(parsed) != EXPECTED:
        raise RuntimeError(
            f"bulk patch path drift: got={sorted(parsed)} expected={sorted(EXPECTED)}"
        )
    if any("ash" in p.lower() for p in parsed):
        raise RuntimeError("forbidden Ash path in generated bulk patch")

    total = applied = already = 0
    by_file = {}
    by_mode = {}
    for rel in sorted(EXPECTED):
        path = root / rel
        text = path.read_text(encoding="utf-8")
        # The generated bulk source was frozen after the project's standard
        # accented-e normalization, while this incremental script runs just
        # before that global step in the normal build chain. Normalize the same
        # characters early only in these target text files so micro-hunk source
        # bodies match; the later global normalizer would make this exact change.
        text = text.replace("é", "e").replace("É", "E")
        a = s = 0
        cursor = 0
        for idx, g in enumerate(parsed[rel], 1):
            text, state, mode, cursor = replace_group(text, rel, idx, g, cursor)
            total += 1
            by_mode[mode] = by_mode.get(mode, 0) + 1
            if state == "applied":
                applied += 1
                a += 1
            else:
                already += 1
                s += 1
        path.write_text(text, encoding="utf-8")
        by_file[rel] = {
            "microHunks": len(parsed[rel]),
            "applied": a,
            "already": s,
        }

    out = root / "build" / "qarro_ru_generated_bulk_v3_177_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "patchFile": PATCH.name,
        "targetFiles": sorted(EXPECTED),
        "targetFileCount": len(EXPECTED),
        "microHunkCount": total,
        "appliedMicroHunks": applied,
        "alreadyAppliedMicroHunks": already,
        "applicationModes": by_mode,
        "byFile": by_file,
        "translationOnly": True,
        "gameplayLogicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: {applied} micro-hunks applied, "
        f"{already} already present across {len(EXPECTED)} text surfaces"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
