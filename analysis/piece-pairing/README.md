# piece-pairing

Two pages from the piece-pairing study: which pieces the players place against each other to keep the board flat.

| directory | page on the site | what it is |
|---|---|---|
| `lookup/` | `ppt2-lookup.html` (方塊落位查表) | Draw a board surface and pick two pieces. The page lists the placements the players chose most often on nearby surfaces, beside Cold Clear's choice. `verify.ts` and `mutant.ts` replay every listed placement through the Tetris engine. |
| `triples/` | `ppt2-triples.html` (三粒痴埋示範) | Shapes of three consecutive pieces that all touch, seen three times or more, played back on the real board. `triples.py` builds `triples.json`. |

`lookup.html` and `triples/demo.html` are page fragments (title, style, body, script). `bin/build-docs` wraps them in a full HTML document (`wrap_study`) and adds them to the index.

The build scripts read per-placement inputs from a scratch directory (`/tmp/...`) that is not committed, so they cannot be re-run from this repo alone. The committed pages and JSON are the outputs. No video is copied; the pages only link to the source videos.
