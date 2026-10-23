"""Random-input robustness test: run each program with random menu choices
and random entries ("", 0, 1, 2, ⁻1, 1/2, X, X-1, {1,⁻1}, 3), and report every
distinct TI math error (DOMAIN, DIVIDE BY 0, INVALID DIM, NONREAL ANS ...).

ERR:SYNTAX and ERR:DATA TYPE are skipped: they come from malformed entries
(a menu digit run into the typed text, a list where a number belongs), which
TI-BASIC cannot trap; MANUAL.md section 15 documents them. A run that
desyncs (typed text arriving at a getKey wait) is skipped too.

    python tests/fuzz.py [seed] [runs]
"""
import collections
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import harness, tibasic
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
progs = "ZCPLX ZQSOLV ZQUAD ZDIV ZPOLY ZZEROS ZRATEQ ZRATFN ZINEQ ZGRAPH ZCHECK".split()
vals = ["", "0", "1", "2", "~1", "1/2", "X", "X-1", "{1,~1}", "3"]
seen = collections.OrderedDict()
for n in range(N):
    prog = random.choice(progs)
    keys = "".join(random.choice("123456") for _ in range(random.randint(0, 2)))
    for _ in range(14):
        keys += random.choice(vals) + "\n"
        if random.random() < 0.3:
            keys += random.choice("123456")
    it = harness.new_interp(keys)
    try:
        it.run(prog)
    except (tibasic.Halt,):
        pass
    except tibasic.TIError as e:
        if "SYNTAX" in str(e) or "DATA TYPE" in str(e):
            continue
        sig = (prog, str(e))
        if sig not in seen:
            seen[sig] = keys
    except RuntimeError:
        pass
for (p, e), k in seen.items():
    print(p, e, repr(k))
print("FUZZ: distinct errors:", len(seen))
sys.exit(1 if seen else 0)
