DIFF={'quad','tss','tsd','tst','tsmini'}
def streaks(seq):
  """seq: list of None (non-clearing lock) | 'BREAK' | kind str. returns (max_combo, max_b2b)"""
  run=0; mc=0; b=-1; mb=0
  for k in seq:
    if k=='BREAK': run=0; b=-1; continue
    if k is None: run=0; continue
    run+=1; mc=max(mc,run-1)
    if k in DIFF: b+=1; mb=max(mb,b)
    else: b=-1
  return mc,max(mb,0)
