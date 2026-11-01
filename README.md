# FlapJax Treasury On-Chain Audits (BSC) — Q76, Q78, Q80

[![CI](https://github.com/ket4min-susan/flapjax-treasury-audits/actions/workflows/ci.yml/badge.svg)](https://github.com/ket4min-susan/flapjax-treasury-audits/actions/workflows/ci.yml) · [GitLab Mirror (`@memwm`)](https://gitlab.com/memwm/flapjax-treasury-audits)

Independent on-chain receipt verification of outbound `FLAPJAX` (`0x90c8889f428F9Ebb77BB8f15CAD3a50a9aC680df`) transfers from the FlapJax treasury (`0x7C34E9e21eE28A49Ff0b84B61774119E6633359f`) on BNB Smart Chain (BSC), grouped by first BNB funder.

- **Worker / BSC Payout Wallet (Taskmarket)**: `0xf46B3853261750F666eB3963e2cB40d6b68938A9`
- **Secondary Operator BSC Wallet**: `0x8403552Cc81858Eb301Efbed64Bb0A25b33EF727`
- **Live Snapshot Block Verified**: `130768956`

## Audit Reports

1. **[Receipt Relay Q76 — 2026-10-27 COT (`TSK-5F4569R1`)](./q76-2026-10-27-audit.md)**
   - Blocks `130029690` (`2026-10-27 00:00:00 COT`) to `130221519` (`2026-10-27 23:59:59 COT`)
   - `31` outbound transfers, `10,147,000 FLAPJAX`, `20` distinct recipients
2. **[Receipt Relay Q78 — 2026-10-28 COT (`TSK-QMV5MMJW`)](./q78-2026-10-28-audit.md)**
   - Blocks `130221520` (`2026-10-28 00:00:00 COT`) to `130413457` (`2026-10-28 23:59:59 COT`)
   - `17` outbound transfers, `2,480,000 FLAPJAX`, `10` distinct recipients
3. **[Receipt Relay Q80 — 2026-10-29 COT (`TSK-RC1MAYQ3`)](./q80-2026-10-29-audit.md)**
   - Blocks `130413458` (`2026-10-29 00:00:00 COT`) to `130605332` (`2026-10-29 23:59:59 COT`)
   - `18` outbound transfers, `5,720,000 FLAPJAX`, `13` distinct recipients

## Reproducibility

- [`verified_transfers.json`](./verified_transfers.json): Full machine-readable dataset of all 66 treasury outbound transfers across `2026-10-27`..`2026-10-29` COT, all verified first-BNB-funder linking transactions, and live recipient state reads at block `130768956`.
- [`verify_all_66_txs.py`](./verify_all_66_txs.py) & [`verify_funders_and_nonces.py`](./verify_funders_and_nonces.py): Zero-dependency Python 3 verification scripts querying public BSC RPC endpoints (`https://bsc-rpc.publicnode.com`, `https://bsc-dataseed.binance.org`, `https://1rpc.io/bnb`).
