# mqpena.github.io

Personal academic website of Malaquías Peña, served by GitHub Pages at <https://mqpena.github.io>.

## Updating

All content lives in `data/`:

| File | Contents |
| --- | --- |
| `data/site.json` | Profile, biography, news, interests, education, research areas, preprints, ongoing studies, projects, teaching, service |
| `data/publications.json` | Journal articles, proceedings, chapters, reports and presentations |
| `data/team.json` | Mentoring record |

After editing, rebuild the pages and commit:

```bash
python3 build.py
git add -A && git commit -m "Update site" && git push
```

`build.py` needs only Python 3 (no packages). Preview locally with `python3 -m http.server` and open <http://localhost:8000>.

## Code for manuscripts

Each ongoing study has its own private repository. When a study is submitted or posted, make its repository public and add `"code": "https://github.com/mqpena/<repo>"` to the matching entry under `preprints` in `data/site.json`.
