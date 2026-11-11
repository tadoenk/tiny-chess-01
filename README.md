# Tiny chess engine

**Owner:** Tadoenk  
**Referral code:** pn0h53j2  
**Repository:** tadoenk/tiny-chess-01  
**Bounty:** https://make.fun/bounty/tiny-chess-01

## What it is

A chess engine in 3,014 bytes of Python (`main.py` is a zlib-compressed payload
with a one-line unpacker, which the rules explicitly allow; the payload and the
unpacker together count toward the 4,096-byte cap). It plays the house gauntlet
through the env at `MAKEFUN_ENV_URL`: 16 games against eight fixed-strength
house engines, weakest first, two games each (white, then black).

## The engine

- 10x12 board (a1=21, h8=98, off-board squares are `#`), so a move off the
  board is a single comparison.
- Full legal move generation: pawns (single and double push, captures, en
  passant, promotion to all four pieces), castling (both sides, with the
  b-file square checked on the queenside), and the king never left in check.
  Validated against the standard perft suites: startpos 20/400/8902,
  Kiwipete 48/2039/97862, and the en-passant, promotion and castling suites
  all exact to depth 3.
- Negamax with alpha-beta pruning, a quiescence search over captures and
  promotions, MVV-LVA capture ordering, a transposition table, and material
  plus piece-square evaluation (six middlegame tables, stored as one character
  per square).
- Iterative deepening under a fixed node budget of 50,000 nodes a move, never
  a clock, so the trial's replay reproduces the live trial move for move.
  About 30,000-67,000 nodes a second in Python, so a move takes well under
  the 10-second limit.

## Run

```bash
MAKEFUN_ENV_URL=<env url> python3 main.py
```

Python 3.13, standard library only. Deterministic: no wall clock, no
unseeded randomness.
