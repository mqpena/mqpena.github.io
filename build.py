#!/usr/bin/env python3
"""Build the static site from data/*.json.

Edit the JSON files, then run:  python3 build.py
The generated *.html files are committed and served directly by GitHub Pages.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
site = json.loads((ROOT / "data/site.json").read_text())
pubs = json.loads((ROOT / "data/publications.json").read_text())
team = json.loads((ROOT / "data/team.json").read_text())
GH = f"https://github.com/{site['github']}"

PAGES = [("index.html", "Home"), ("publications.html", "Publications"),
         ("research.html", "Research"), ("teaching.html", "Teaching"),
         ("team.html", "Team")]

ICON_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="m3 6 9 7 9-7" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
ICON_GH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .5a11.5 11.5 0 0 0-3.6 22.4c.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.5-3.9-1.5-.5-1.3-1.3-1.7-1.3-1.7-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.7-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.2 1.2a11 11 0 0 1 5.8 0c2.2-1.5 3.2-1.2 3.2-1.2.6 1.6.2 2.8.1 3.1.8.8 1.2 1.8 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A11.5 11.5 0 0 0 12 .5Z"/></svg>'


def page(fname, title, body):
    nav = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if f == fname else ""}>{t}</a>'
        for f, t in PAGES)
    full_title = site["name"] if fname == "index.html" else f"{title} · {site['name']}"
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(site['name'])}, {escape(site['title'])}, {escape(site['affiliation'])}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<script>try{{const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="index.html">{escape(site['name'])}</a>
<nav>{nav}</nav>
<button class="theme" type="button" aria-label="Toggle light or dark theme" onclick="toggleTheme()">◐</button>
</div></header>
<main class="wrap">
{body}
</main>
<footer class="wrap">© 2026 {escape(site['name'])} · Built with a small static generator · <a href="{GH}/{site['github']}.github.io">Source</a></footer>
<script>
function toggleTheme(){{const r=document.documentElement;const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark';try{{localStorage.setItem('theme',r.dataset.theme)}}catch(e){{}}}}
</script>
</body>
</html>
"""
    (ROOT / fname).write_text(html)


def link(label, url):
    return f'<a class="pill" href="{escape(url)}">{label}</a>' if url else ""


def entry(e):
    links = link("Paper", e.get("paper")) + link("Code", e.get("code"))
    return (f'<li class="pub"><div class="authors">{e["authors"]} ({e["year"]})</div>'
            f'<div class="ptitle">{escape(e["title"])}</div>'
            f'<div class="venue">{e["venue"]}</div>'
            f'{f"<div class=links>{links}</div>" if links else ""}</li>')


def ongoing(e):
    repo = (f'<span class="pill muted" title="Private repository, opened on submission">Code: private until submission</span>'
            if e.get("repo") else "")
    return (f'<li class="pub"><div class="authors">{e["authors"]}</div>'
            f'<div class="ptitle">{escape(e["title"])}</div>'
            f'<div class="venue">{escape(e["summary"])}</div>'
            f'{f"<div class=links>{repo}</div>" if repo else ""}</li>')


def cite(e):
    t = escape(e["text"]).replace("Peña, M.", "<b>Peña, M.</b>").replace("M. Peña", "<b>M. Peña</b>")
    return f'<li>{t}{" " + link("Link", e["url"]) if e.get("url") else ""}</li>'


# ---------- Home ----------
initials = "".join(w[0] for w in site["name"].split())
home = f"""
<section class="profile">
  <div class="avatar" aria-hidden="true">{initials}</div>
  <div>
    <h1>{escape(site['name'])}</h1>
    <p class="role">{escape(site['title'])}<br><a href="{site['affiliation_url']}">{escape(site['affiliation'])}</a></p>
    <p class="icons"><a href="mailto:{site['email']}" aria-label="Email">{ICON_MAIL}<span>{site['email']}</span></a>
    <a href="{GH}" aria-label="GitHub">{ICON_GH}<span>{site['github']}</span></a></p>
  </div>
</section>
<section><h2>Biography</h2>{''.join(f'<p>{p}</p>' for p in site['bio'])}</section>
<section class="cols">
  <div><h2>Interests</h2><ul class="plain">{''.join(f'<li>{escape(i)}</li>' for i in site['interests'])}</ul></div>
  <div><h2>Education</h2><ul class="plain">{''.join(f'<li><b>{escape(a)}</b><br><span class="dim">{escape(b)}</span></li>' for a, b in site['education'])}</ul></div>
</section>
<section><h2>Recent news</h2><table class="news">{''.join(f'<tr><th scope="row">{d}</th><td>{t}</td></tr>' for d, t in site['news'])}</table></section>
<section><h2>Preprints and submitted manuscripts</h2><ul class="pubs">{''.join(entry(e) for e in site['preprints'])}</ul></section>
<section><h2>Ongoing studies</h2><p class="dim">Studies in preparation with collaborators. Manuscripts and code are kept in private repositories and will be released with each submission.</p>
<ul class="pubs">{''.join(ongoing(e) for e in site['ongoing'])}</ul></section>
<p><a href="publications.html">All publications →</a></p>
"""
page("index.html", "Home", home)

# ---------- Publications ----------
years = sorted({e["year"] for e in pubs["journal"] if e["year"]}, reverse=True)
pub_body = '<h1>Publications</h1>'
pub_body += f'<section><h2>Preprints and submitted</h2><ul class="pubs">{"".join(entry(e) for e in site["preprints"])}</ul></section>'
pub_body += '<section><h2>Journal articles</h2>'
for y in years:
    pub_body += f'<h3 class="year">{y}</h3><ol class="cites">{"".join(cite(e) for e in pubs["journal"] if e["year"] == y)}</ol>'
pub_body += '</section>'
for key, head in [("proceedings", "Conference proceedings"), ("chapters", "Book chapters"),
                  ("reports", "Reports and workshop contributions")]:
    pub_body += f'<section><h2>{head}</h2><ol class="cites">{"".join(cite(e) for e in pubs[key])}</ol></section>'
pub_body += '<section><h2>Presentations</h2>'
for key, head in [("oral", "Selected oral presentations"), ("invited", "Selected invited talks"),
                  ("conference", "Selected conference presentations")]:
    pub_body += f'<h3>{head}</h3><ol class="cites">{"".join(cite(e) for e in pubs[key])}</ol>'
pub_body += '</section>'
page("publications.html", "Publications", pub_body)

# ---------- Research ----------
res = '<h1>Research</h1><div class="cards">'
res += "".join(f'<article class="card"><h2>{escape(h)}</h2><p>{escape(t)}</p></article>' for h, t in site["areas"])
res += '</div><section><h2>Sponsored projects</h2><p class="dim">Support from NOAA, NSF, DOE, ONR, Eversource Energy, Bay State Wind and UConn OVPR.</p>'
res += '<div class="tablewrap"><table class="grid"><thead><tr><th>Role</th><th>Sponsor</th><th>Project</th><th>Period</th></tr></thead><tbody>'
res += "".join(f'<tr><td>{r}</td><td>{escape(s)}</td><td>{escape(p)}</td><td class="nowrap">{t}</td></tr>' for r, s, p, t in site["projects"])
res += '</tbody></table></div></section>'
res += f'<section><h2>Code</h2><p>Public research software is on <a href="{GH}">GitHub</a>, including <a href="{GH}/logistic-error-growth-limits">logistic-error-growth-limits</a> for the NPG preprint. Code for ongoing studies is released with each submission.</p></section>'
page("research.html", "Research", res)

# ---------- Teaching ----------
tea = '<h1>Teaching</h1><p>Founder and director of UConn\'s graduate online <b>Power Grid Modernization Certificate</b> (2020–2024), working with employer-supported cohorts.</p>'
tea += '<section><h2>Courses</h2><ul class="plain">' + "".join(f'<li><b>{escape(c)}</b><br><span class="dim">{escape(w)}</span></li>' for c, w in site["teaching"]) + '</ul></section>'
tea += '<section><h2>Professional service</h2><ul>' + "".join(f'<li>{s}</li>' for s in site["service"]) + '</ul></section>'
page("teaching.html", "Teaching", tea)

# ---------- Team ----------
tm = '<h1>Team</h1><p class="dim">Mentoring record as of July 2026.</p>'
for key, head in [("major", "Major advisor"), ("associate", "Associate advisor"), ("external", "External associate advisor")]:
    tm += f'<section><h2>{head}</h2><ul class="plain">'
    for line in team[key]:
        name, _, rest = line.partition(" (")
        tm += f'<li><b>{escape(name)}</b> <span class="dim">({escape(rest)}</span></li>'
    tm += '</ul></section>'
page("team.html", "Team", tm)

print("Built", ", ".join(f for f, _ in PAGES))
