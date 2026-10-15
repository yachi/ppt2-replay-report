# ko2 copy of endfix/fixA/endfix_a.py (Y set, j009/j010): fallback ONLY when find_end returns None — same rule with
# the winner threshold at 0.4. The fallback frame now goes through analyze_ko2.refine like the main path.
def install(Am):
    orig = Am.find_end
    def find_end(border, lo, hi):
        f, p = orig(border, lo, hi)
        if f is not None: return f, p
        f, p = Am._detect(border, lo, hi, winner_min=0.4)
        return Am.refine(border, f, p), p
    Am.find_end = find_end
