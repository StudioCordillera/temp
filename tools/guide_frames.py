"""Record the screens the field guide's replay calculators show.

Each scenario is a real program run in the harness with a key script. The
script is cut into steps (a menu choice, a typed entry, its ENTER, a page
key), and the program is re-run from the start for every prefix, so each
frame is exactly what the calculator shows at that point. Graph pages are
captured from the drawing commands ZLSHOW issues, with the function sampled
by the interpreter itself.

    python tools/guide_frames.py            writes build/guide-frames.json
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
import harness  # noqa: E402
import tibasic  # noqa: E402
from tibasic import D  # noqa: E402

# id: (program, title, keys). Keys: \n ENTER, ~ (-), # CLEAR, < up.
SCENARIOS = {
    "mk-launch": ("MATHKIT", "Open ZCPLX from the launcher", "1"),
    "mk-settings": ("MATHKIT", "Switch to answer only", "72"),
    "cx-1e": ("ZCPLX", "Form B 1e, every page", "1~12\n~1\n144\n~4\n\n\n\n\n"),
    "cx-2e": ("ZCPLX", "Form B 2e, multiply", "48\n~1\n9\n4\n1\n16\n#"),
    "qs-8d": ("ZQSOLV", "Form B 8d, typed", "5(~2+3X)²\n47\n1\n\n\n"),
    "qs-12i": ("ZQSOLV", "Form B 12i, formula", "42\n10\n0\n0\n0\n~3\n#"),
    "qs-10c": ("ZQSOLV", "Form B 10c, fractions", "21\n~1/4\n0\n~13/16\n#"),
    "qd-9b": ("ZQUAD", "Form B 9b, every page", "11\n~6\n~7\n\n\n\n\n\n\n\n\n\n\n\n"),
    "qd-15": ("ZQUAD", "Form B 15, application", "4~4.9\n29.4\n78.4\n1#"),
    "qd-4": ("ZQUAD", "Form B 4, from a graph", "3~3\n2\n~5\n0\n#"),
    "dv-17a": ("ZDIV", "Form B 17a, synthetic", "1{4,~7,~18,9}\n3\n\n\n\n\n\n"),
    "dv-16d": ("ZDIV", "Form B 16d, long division", "2X^5+3X^4-2X²-X-8\nX²-2\n#"),
    "pl-25": ("ZPOLY", "Form B 25, factored form", "22\n2\n1\n5\n1\n1\n2\n2\n#"),
    "pl-21": ("ZPOLY", "Form B 21, zeros and a point", "33\n~3\n1\n1\n1\n4\n1\n0\n0\n2\n#"),
    "zz-28c": ("ZZEROS", "Form B 28c, given a zero", "1{2,~5,~21,36}\n~3\n0\n\n\n\n\n"),
    "zz-29f": ("ZZEROS", "Form B 29f, find all", "2{4,~1,~44,11}\n#"),
    "zz-27e": ("ZZEROS", "Form B 27e, complex zero", "1{1,2,1,18,~72}\n0\n3\n#"),
    "re-30f": ("ZRATEQ", "Form B 30f, every page", "12\n1\n11\nX-3\n~8\nX+3\n9\nX²-9\n\n\n\n\n\n\n\n"),
    "re-30c": ("ZRATEQ", "Form B 30c, extraneous root", "12\n1\n1\nX\n1\nX-5\nX-4\nX-5\n#<"),
    "rf-31d": ("ZRATFN", "Form B 31d, analyze", "2X²+7X+3\nX²-9\n1#"),
    "rf-34": ("ZRATFN", "Form B 34a and 34c", "{1,0,0}\n{~60,3600}\n248\n#\n55N\n"),
    "iq-41g": ("ZINEQ", "Form B 41g, typed", "1X³+10X²+27X\n~18\n4#"),
    "iq-44": ("ZINEQ", "Form B 44, rational", "33X-2\n(X+2)²\n4\n\n\n\n"),
    "iq-42b": ("ZINEQ", "Form B 42b, from a graph", "41\n2\n2\n1\n~4\n1\n6\n1\n22#"),
    "gr-32a": ("ZGRAPH", "Form B 32a, graph 1/x", "252~1\n~3\n4\n\n\n\n\n\n"),
    "gr-pts": ("ZGRAPH", "Poly through 4 points", "44\n0\n1\n1\n0\n2\n5\n3\n22\n#"),
    "ck-12j": ("ZCHECK", "Check x=1/3 in 12j", "3X²+8X-3=0\n11/3\n#"),
    "ck-guard": ("ZCHECK", "An excluded value", "1/(X-5)\n2{5}\n5\n#"),
}


def run(prog, keys):
    """Run once; return the interpreter, the wait reason and any graph shown."""
    it = harness.new_interp(keys)
    state = {"graph": None}
    cmds = dict(tibasic.Interp.COMMANDS)

    def home(name):
        f = cmds[name]

        def g(self, fr, i, s):
            state["graph"] = None
            return f(self, fr, i, s)
        return g

    def graph(self, fr, i, s):
        cmds["Text("](self, fr, i, s)
        last = self.graph_log[-1]
        if last.startswith("Text(150"):
            state["graph"] = capture(self)

    it.COMMANDS = dict(cmds)
    for name in ("ClrHome", "Disp ", "Output("):
        it.COMMANDS[name] = home(name)
    it.COMMANDS["Text("] = graph
    reason, error = None, None
    try:
        it.run(prog)
        reason = "end"
    except tibasic.Halt:
        reason = it.waiting_reason
    except tibasic.TIError as e:
        error = str(e)
    return it, reason, state["graph"], error


def capture(it):
    """The graph page as data: window, sampled curve, asymptotes, points, title."""
    w = {k: float(it.window[k]) for k in ("Xmin", "Xmax", "Ymin", "Ymax")}
    log = it.graph_log
    start = max(i for i, t in enumerate(log) if t == "ClrDraw")
    va, pts, title = [], [], ""
    for t in log[start:]:
        if t.startswith("Vertical "):
            va.append(float(t[len("Vertical "):].replace("⁻", "-")))
        elif t.startswith("Pt-On("):
            a = t[len("Pt-On("):].replace("⁻", "-").split(",")
            pts.append([float(a[0]), float(a[1])])
        elif t.startswith("Text(1,1,"):
            title = t[len("Text(1,1,"):]
    expr = it.strs["Str6"]
    saved = it.vars["X"]
    curve = []
    n = 264
    for k in range(n + 1):
        x = w["Xmin"] + (w["Xmax"] - w["Xmin"]) * k / n
        it.vars["X"] = D(repr(x))
        try:
            v = it.eval_tokens(list(expr))
            y = float(v) if isinstance(v, D) else None
        except (tibasic.TIError, TypeError, ValueError):
            y = None
        curve.append(None if y is None else round(y, 4))
    it.vars["X"] = saved
    return {"win": w, "va": va, "pts": pts, "title": title, "expr": "".join(expr),
            "curve": curve}


def frames(prog, keys):
    out = []
    i = 0
    label = None
    while True:
        it, reason, graph, error = run(prog, keys[:i])
        if error:
            raise SystemExit(f"{prog} {keys[:i]!r}: {error}")
        rows = [("".join(r)) for r in it.screen]
        fr = {"rows": rows, "wait": reason, "key": label}
        if reason == "Menu":
            fr["menu"] = True
        if graph:
            fr["graph"] = graph
        out.append(fr)
        if i >= len(keys):
            break
        if reason == "Input":
            j = keys.find("\n", i)
            if j > i:
                label = {"k": "type", "t": keys[i:j].replace("~", "⁻"), "prompt": prompt_of(rows)}
                i = j
                continue
            label = {"k": "enter", "prompt": prompt_of(rows)}
            i += 1
            continue
        ch = keys[i]
        if reason == "Menu":
            n = int(ch) if ch.isdigit() else 1
            item = rows[n].strip() if n < len(rows) else ch
            label = {"k": "menu", "t": ch, "item": item.split(":", 1)[-1], "title": rows[0].strip()}
        else:
            label = {"k": {"\n": "enter", "#": "clear", "<": "up", ">": "down"}.get(ch, ch)}
            if ch.isalpha() or ch.isdigit():
                label = {"k": "key", "t": ch}
        i += 1
    return out


def prompt_of(rows):
    """The prompt on the line where the cursor waits (the last non-blank row)."""
    for r in reversed(rows):
        if r.strip():
            return r.rstrip()
    return ""


def main():
    data = {}
    for sid, (prog, title, keys) in SCENARIOS.items():
        fs = frames(prog, keys)
        data[sid] = {"prog": prog, "title": title, "frames": fs}
        print(f"{sid:10} {prog:8} {len(fs):3} frames  last: {fs[-1]['rows'][0].strip()}")
    path = os.path.join(ROOT, "build", "guide-frames.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
