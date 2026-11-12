# Tiny Chess 01 - make.fun Submission

This repository contains our entry for the **make.fun tiny-chess-01** competition. The challenge requires building a fully functional chess engine whose entrypoint `main.py` is at most 4,096 bytes and plays chess games via an environment server at `MAKEFUN_ENV_URL`.

## Engine Design (`engine.py`)

- **Board Representation:** 0x88 board layout (`0x88` structure for efficient move generation and out-of-bounds checks).
- **Search:** Negamax alpha-beta search with transposition table, killer-move ordering, and quiescence search covering captures, promotions, and check replies.
- **Move Ordering & MVV-LVA:** MVV-LVA (Most Valuable Victim - Least Valuable Aggressor) capture scoring combined with killer moves.
- **Evaluation:** Incremental piece-square table evaluation with an endgame king-table interpolation driven by remaining non-pawn material, along with a bishop-pair bonus.
- **Budget:** Fixed 100,000-node node budget per search iteration for deterministic play.

## Environment Interaction

The engine communicates with the competition environment server over HTTP using `urllib.request`. It queries `/game` to retrieve the game state and `/move` to submit moves decided by the iterative deepening search (`ch` function).

## Packing Mechanism (`pack.py`)

To ensure `main.py` stays well under the 4,096-byte limit, `pack.py` compiles `engine.py` into a compact self-extracting runner:
1. Reads `engine.py` as bytes.
2. Compresses using raw-deflate (`zlib.compressobj(9, zlib.DEFLATED, -15)`).
3. Encodes the compressed stream using base85 (`base64.b85encode`).
4. Generates a single-line `main.py` entrypoint:
   ```python
   import zlib,base64;exec(zlib.decompress(base64.b85decode('<blob>'),-15))
   ```
5. Prints the exact byte size of `main.py`.

## Verification

- **`main.py` Byte Size (before header):** 3,664 bytes (limit: 4,096 bytes).
- **`main.py` Byte Size (with header):** 3,744 bytes (limit: 4,096 bytes).
- **Syntax Check:** `python3 -m py_compile main.py engine.py pack.py` passed successfully.
- **Perft Smoke Test:** `perft_smoke.py` completed all test positions successfully (**PERFT ALL OK**).
- **Payload Integrity:** Extracted base85 payload from `main.py` (skipping header line), decompressed with raw deflate (`wbits=-15`), and verified byte-for-byte match with `engine.py` (**PAYLOAD MATCHES ENGINE**).
