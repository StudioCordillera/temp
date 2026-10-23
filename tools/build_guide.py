"""Build MATHKIT-Field-Guide.html from tools/guide_template.html.

Fills the template with screens recorded from the real programs:
  <!--PAGES id-->     the title of every work page of scenario id
  <!--SNAP id n-->    a static screen: frame n (negative counts from the end),
                      or pN for the first frame showing page N
  /*FRAMES*/          the replay frames (build/guide-frames.json)

    python tools/build_guide.py [fragment.html]

Writes MATHKIT-Field-Guide.html (a complete page that also loads Mermaid),
and, if a path is given, the same page as a fragment for publishing as a
claude.ai artifact (which supplies its own document wrapper and Mermaid).
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import guide_frames  # noqa: E402

PAGE = re.compile(r"^(\d+)/(\d+) ")


def first_page_keys(prog, keys):
    """The input part of a scenario: keys up to the first work page."""
    base = keys.split("#")[0].rstrip("\n<")
    for extra in range(0, 4):
        k = base + "\n" * extra
        it, _, graph, _ = guide_frames.run(prog, k)
        row = "".join(it.screen[0]).strip()
        if PAGE.match(row) and row.startswith("1/"):
            return k
    raise SystemExit(f"no first page for {prog} {keys!r}")


def page_titles(prog, keys):
    base = first_page_keys(prog, keys)
    it, _, _, _ = guide_frames.run(prog, base)
    total = int(PAGE.match("".join(it.screen[0]).strip()).group(2))
    titles = []
    for k in range(total):
        it, _, graph, _ = guide_frames.run(prog, base + "\n" * k)
        row = graph["title"] if graph else "".join(it.screen[0]).strip()
        titles.append(row)
    return titles


def lcd_text(s):
    return html.escape(s).replace("𝑖", '<span class="ii">i</span>')


def pages_html(prog, keys):
    out = ['<ol class="pages">']
    for t in page_titles(prog, keys):
        m = PAGE.match(t)
        num, rest = (t[:m.end()].strip(), t[m.end():]) if m else ("", t)
        cls = ' class="ans"' if rest.startswith("ANSWER") else ""
        out.append(f"<li{cls}><b>{html.escape(num)}</b>{lcd_text(rest)}</li>")
    out.append("</ol>")
    return "".join(out)


def snap_html(frames, which):
    if which.startswith("p"):
        n = which[1:]
        f = next(f for f in frames if "".join(f["rows"][0]).startswith(n + "/"))
    else:
        f = frames[int(which)]
    rows = [r.rstrip() for r in f["rows"]]
    return '<pre class="scr">' + "\n".join(lcd_text(r) for r in rows) + "</pre>"


def main():
    guide_frames.main()
    data = json.load(open(os.path.join(ROOT, "build", "guide-frames.json"), encoding="utf-8"))
    src = open(os.path.join(ROOT, "tools", "guide_template.html"), encoding="utf-8").read()

    def pages(m):
        sid = m.group(1)
        prog, _, keys = guide_frames.SCENARIOS[sid]
        return pages_html(prog, keys)

    def snap(m):
        return snap_html(data[m.group(1)]["frames"], m.group(2))

    src = re.sub(r"<!--PAGES (\S+)-->", pages, src)
    src = re.sub(r"<!--SNAP (\S+) (\S+)-->", snap, src)
    frames = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    src = src.replace("/*FRAMES*/", frames)
    head, body = src.split("<!--BODY-->")

    full = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>html,body{margin:0}[hidden]{display:none!important}'
            ':root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>\n'
            + head + "</head><body>\n" + body +
            '\n<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>\n'
            '<script>if(window.mermaid){var d=document.documentElement.getAttribute("data-theme");'
            'var dk=d?d==="dark":matchMedia("(prefers-color-scheme: dark)").matches;'
            'mermaid.initialize({startOnLoad:true,theme:dk?"dark":"neutral"});}</script>\n</body></html>\n')
    out = os.path.join(ROOT, "MATHKIT-Field-Guide.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(full)
    print("wrote", out, os.path.getsize(out), "bytes")
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as fh:
            fh.write(head + body)
        print("wrote", sys.argv[1])


if __name__ == "__main__":
    main()
