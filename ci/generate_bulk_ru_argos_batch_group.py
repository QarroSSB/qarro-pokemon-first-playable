#!/usr/bin/env python3
from __future__ import annotations
import os
import generate_bulk_ru_argos_batched as g

targets=[x for x in os.environ["QARRO_TARGETS"].split(";") if x]
g.TARGET_ASM=[x for x in targets if x.startswith("data/") and x.endswith(".inc")]
g.TARGET_C=[x for x in targets if x not in g.TARGET_ASM]
if __name__=="__main__":
    raise SystemExit(g.main())
