#!/usr/bin/env python3
"""Convert the collated Markdown source into HTML for pasting into Google Docs.

Design constraints:

* Google Docs preserves real HTML tables, headings, bold and monospace on paste,
  but mangles Markdown pipe tables into plain text. So the paste source is HTML.
* The Auto-LaTeX Equations add-on scans the pasted document for $$...$$ and
  replaces each occurrence with a rendered image. So every display equation is
  emitted as literal $$...$$ text and left unrendered here.
* Multi-line LaTeX is joined onto one line, because the add-on matches
  delimiters within a single paragraph.
"""

import html
import re
import sys
from pathlib import Path

# Greek spelled out in inline code spans reads badly in a prose document.
# Substituted only inside code spans, never inside $$...$$ LaTeX.
GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ",
    "epsilon": "ε", "theta": "θ", "lambda": "λ", "mu": "μ",
    "nu": "ν", "pi": "π", "rho": "ρ", "sigma": "σ",
    "tau": "τ",
}
# Matches a greek name as a whole symbol, including when a subscript or
# superscript follows (tau_H, pi_s, sigma^2), but never inside an English
# word ("pipeline", "must", "numerator"). \b would fail on "tau_H",
# because the underscore is itself a word character.
GREEK_RE = re.compile(r"(?<![A-Za-z])(" + "|".join(GREEK) + r")(?![A-Za-z])")


def code_text(raw: str) -> str:
    return GREEK_RE.sub(lambda m: GREEK[m.group(1)], raw)


def inline(text: str) -> str:
    """Escape, then apply code spans, bold, italics and links."""
    out, spans = text, []

    def stash(markup: str) -> str:
        spans.append(markup)
        return f"\x00{len(spans) - 1}\x00"

    out = re.sub(r"`([^`]+)`",
                 lambda m: stash(f"<code>{html.escape(code_text(m.group(1)))}</code>"),
                 out)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                 lambda m: stash(
                     f'<a href="{html.escape(m.group(2), quote=True)}">'
                     f"{html.escape(m.group(1))}</a>"),
                 out)
    out = html.escape(out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", out)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], out)


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Fenced blocks: math becomes literal $$...$$, everything else <pre>.
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            body: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            if lang == "math":
                latex = " ".join(s.strip() for s in body if s.strip())
                out.append(f'<p class="eq">$$ {html.escape(latex)} $$</p>')
            else:
                out.append("<pre>" + html.escape("\n".join(body)) + "</pre>")
            continue

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"(#{1,6})\s+(.*)", stripped)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        # Table: header row followed by a |---|---| separator.
        if (stripped.startswith("|") and i + 1 < len(lines)
                and re.fullmatch(r"\|[\s:|-]+\|", lines[i + 1].strip())):
            header = split_row(stripped)
            aligns = ["right" if c.endswith(":") else "left"
                      for c in split_row(lines[i + 1].strip())]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            t = ["<table>", "<thead><tr>"]
            for n, cell in enumerate(header):
                a = aligns[n] if n < len(aligns) else "left"
                t.append(f'<th style="text-align:{a}">{inline(cell)}</th>')
            t.append("</tr></thead><tbody>")
            for row in rows:
                t.append("<tr>")
                for n, cell in enumerate(row):
                    a = aligns[n] if n < len(aligns) else "left"
                    t.append(f'<td style="text-align:{a}">{inline(cell)}</td>')
                t.append("</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        if stripped.startswith("> "):
            body = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                body.append(lines[i].strip()[2:])
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(body))}</p></blockquote>")
            continue

        # Lists. Source is flat apart from occasional two-space continuations.
        m = re.match(r"(\d+)\.\s+(.*)", stripped)
        if m or stripped.startswith("- "):
            ordered = bool(m)
            pat = r"\d+\.\s+(.*)" if ordered else r"-\s+(.*)"
            items: list[str] = []
            while i < len(lines):
                s = lines[i].strip()
                mm = re.fullmatch(pat, s)
                if mm:
                    items.append(mm.group(1))
                elif s and items and lines[i].startswith(("  ", "\t")):
                    items[-1] += " " + s          # wrapped continuation line
                else:
                    break
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items)
                       + f"</{tag}>")
            continue

        # Paragraph: consume until a blank line or a block-level marker.
        body = []
        while i < len(lines):
            s = lines[i].strip()
            if (not s or s.startswith(("#", "|", "```", "> ", "- ", "---"))
                    or re.match(r"\d+\.\s", s)):
                break
            body.append(s)
            i += 1
        out.append(f"<p>{inline(' '.join(body))}</p>")

    return "\n".join(out)


CSS = """
body { font-family: Georgia, 'Times New Roman', serif; font-size: 11pt;
       line-height: 1.45; color: #111; max-width: 46em; margin: 2em auto;
       padding: 0 1em; }
h1 { font-size: 20pt; margin: 0 0 .3em; }
h2 { font-size: 15pt; margin: 1.6em 0 .4em; border-bottom: 1px solid #ccc;
     padding-bottom: .15em; }
h3 { font-size: 12.5pt; margin: 1.3em 0 .3em; }
h4 { font-size: 11pt; margin: 1.1em 0 .25em; font-style: italic; }
p { margin: .55em 0; }
code { font-family: 'Courier New', monospace; font-size: 10pt;
       background: #f4f4f4; padding: 0 .2em; }
pre { font-family: 'Courier New', monospace; font-size: 9.5pt;
      background: #f4f4f4; padding: .7em; white-space: pre-wrap; }
p.eq { font-family: 'Courier New', monospace; font-size: 10pt;
       text-align: center; background: #fbfbfb; padding: .5em; margin: .8em 0; }
table { border-collapse: collapse; width: 100%; margin: .8em 0;
        font-size: 9.5pt; font-family: Arial, Helvetica, sans-serif; }
th, td { border: 1px solid #bbb; padding: .35em .5em; vertical-align: top; }
th { background: #eee; font-weight: bold; }
blockquote { margin: .8em 0; padding: .4em 1em; border-left: 3px solid #888;
             background: #fafafa; }
li { margin: .25em 0; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
"""


def main() -> None:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    body = convert(src.read_text())
    dst.write_text(
        "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\">"
        "<title>SPL Automation Economics</title>"
        f"<style>{CSS}</style></head>\n<body>\n{body}\n</body></html>\n"
    )
    eqs = body.count('class="eq"')
    print(f"wrote {dst} ({len(body):,} bytes of HTML, {eqs} equations)")


if __name__ == "__main__":
    main()
