#!/usr/bin/env bash
set -euo pipefail
EXPECTED_BASE_CANDIDATES="${EXPECTED_BASE_CANDIDATES:-3881}"
mkdir -p kit/normalized_parts
python3 - <<'PY'
from pathlib import Path
import hashlib
expected = [
    ('part00', 6000, '3e940e9b1a1d3b1ef4a4414a1a1fa943a76daecdee7bc7298c28d42dbfdf4ce6'),
    ('part01', 6000, 'e94329bbc06c3c5b957cb61bdd7d598866fb2491682d6057d54d5d8ad6c0ac54'),
    ('part02', 6000, '166ecb7390b18d9880810dd9e9e2b5bb2a14609cb94a2a35967cd397b0c218d7'),
    ('part03', 6000, '70a4fa13ef17c2778aeffb53dea204476003c202372e25c87e71c3a2d18002ee'),
    ('part04', 6000, '4bcc27379e86b2ce3ce3b8183a47ba355406349e4a79b68fc826b4bf474f1321'),
    ('part05', 5320, '25b0c7a8c5ba212ffa5740107a14d5c94a3f1fddc4c3ccc84d08989c5c21779e'),
]
srcdir=Path('qarro-repo/kit_parts'); outdir=Path('kit/normalized_parts')
for short, expected_len, expected_sha in expected:
    data=(srcdir/f'qarro_kit_v3_0.{short}.b64').read_bytes()
    if hashlib.sha256(data).hexdigest()==expected_sha:
        fixed=data
    elif len(data)==expected_len+1:
        fixed=None
        for i in range(len(data)):
            c=data[:i]+data[i+1:]
            if hashlib.sha256(c).hexdigest()==expected_sha:
                fixed=c; break
        if fixed is None: raise SystemExit(f'{short}: repair failed')
    else: raise SystemExit(f'{short}: checksum/size mismatch')
    (outdir/f'{short}.b64').write_bytes(fixed)
PY
cat kit/normalized_parts/part*.b64 > kit/qarro_kit_text.tar.gz.b64
echo "19e30690575cf31d941f9e183c7e52f452238a4d18759577c520909a718e01c1  kit/qarro_kit_text.tar.gz.b64" | sha256sum -c -
base64 -d kit/qarro_kit_text.tar.gz.b64 > kit/qarro_kit_text.tar.gz
echo "95ca1dd309d79ecfed86e21b441725c8b68b7ec0368efc33dcf790be0d62eed9  kit/qarro_kit_text.tar.gz" | sha256sum -c -
tar -xzf kit/qarro_kit_text.tar.gz -C kit

python3 kit/Source_Migration/v3_0/tools/install_first_playable_v3_0.py upstream
python3 qarro-repo/ci/content_pass_v3_1.py upstream
python3 qarro-repo/ci/runtime_content_v3_3.py upstream
python3 qarro-repo/ci/qol_v3_5.py upstream
python3 qarro-repo/ci/install_cyrillic_v3_3.py upstream
python3 qarro-repo/ci/localization_ru_core_v3_3.py upstream
python3 qarro-repo/ci/localize_early_kanto_v3_9.py upstream
python3 qarro-repo/ci/localize_cerulean_misty_v3_22.py upstream
python3 qarro-repo/ci/localize_oaks_lab_starter_v3_5.py upstream
python3 qarro-repo/ci/sanitize_ru_quotes_v3_18.py upstream
python3 qarro-repo/ci/normalize_accented_e_v3_8.py upstream
python3 qarro-repo/ci/audit_ru_runtime_surface_v3_21.py upstream
python3 - <<'PY'
import json,os
j=json.load(open('upstream/build/qarro_ru_runtime_surface_v3_21_audit.json',encoding='utf-8'))['fullSurface']
exp=int(os.environ.get('EXPECTED_BASE_CANDIDATES','3881'))
print('base',j['englishOnlyCandidateCount'],j['filesWithCandidates'])
if j['englishOnlyCandidateCount']!=exp:
    raise SystemExit(f"expected {exp}, got {j['englishOnlyCandidateCount']}")
PY
git -C upstream config user.name "Qarro Fast Translation Generator"
git -C upstream config user.email "actions@users.noreply.github.com"
git -C upstream add -A
git -C upstream commit -m "Qarro FULL GREEN v3.173 reproduced base"
