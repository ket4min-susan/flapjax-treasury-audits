import json
import urllib.request
import sys
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding="utf-8")

RPC_URLS = [
    "https://bsc-rpc.publicnode.com",
    "https://bsc-dataseed.binance.org",
    "https://1rpc.io/bnb",
]

def rpc_call(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
    for url in RPC_URLS:
        try:
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "flapjax-auditor/1.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "result" in data and data["result"] is not None:
                    return data["result"]
        except Exception:
            continue
    raise RuntimeError(f"All RPCs failed for {method} {params}")

# Let's verify the first-funder transactions mentioned across all 3 days + boundary txs
funder_txs = {
    "0x805757cc16164c3a4f9301e6e8ad1ab431c054597d748345123b54e1c46661c3": "0x8186bdC89E5893393136265f88bA3719BF453527 (Treasury BNB drip)",
    "0x87443eff758296585f6d6eb7b68800ea6c73f143239e60541a6ef5b1f072d456": "0xCa58696564492eF9C3229c89072365b253bda246 (Treasury BNB drip, nonce 500)",
    "0xa3d7042983f4f2352b9b8f324414688db10887e2b2b2a125deca9a8bec6624e7": "0xFB200657F7266157A45Dfcc6c09690726Daa24E6 (Treasury BNB drip)",
    "0xb5a5215482c7cade369d789258eb4da375a32d62aa0392d669e56256d6d36ed8": "0x8c062Dc5D775B7D5efc168F75a875f392f53dCdf",
    "0x98555eda02f315f4530ffb7f0f8766ef399afecff849e2eb84cf5bd63c660b34": "0xd1caDa310f73455a2B119fa49aA8B682bFFF9F7D",
    "0x16b9ff162d92e744fdecc76c60fd2126f07b938eecca40305049735b9408e4aa": "0xc39A62559E81807e0F63C0529dA375CFC8fb294c",
    "0x9f29671af3eea3cdd07dd18cbd4828fe4fab342ba65a69fd79ef5e703d9da9bb": "0xC3B4F10bC4c4A64676b398EBbe23b29440dcA40c",
    "0x3e5194c19461d50f30f68b61e9979980597e122f331066cef841e6583fb93ad6": "0x6e850F8549f2490E26d86F43F80594565f0f00A3",
    "0x322f5447e749887d2ea22c54536959d2a9f06890005c0ac2306d368e265c5840": "0xA21fc88Bd8C17CaE306089d7B00a1f5CD5AD3eE9",
    "0x4ebb6e4d294ff40d30295c857f3b19bae19bf73b3fb0d71fa4944362dfa49e79": "0xAB39Aa1e2db4036e01CF7e919b3f239b3ff90160 (internal call)",
    # Boundary txs
    "0xe3a4e799eb637256215475edef4ef2b3580742c5ce2cad45eabc4f75e8529399": "Last OUT before Oct 27",
    "0x8aaafffe50593fa7a42cca7d9c12c8e8459f05268add27612faaea557be7d4f8": "First OUT after Oct 29",
}

verified_funders = {}
for tx_hash, desc in funder_txs.items():
    tx = rpc_call("eth_getTransactionByHash", [tx_hash])
    rcpt = rpc_call("eth_getTransactionReceipt", [tx_hash])
    blk = int(tx["blockNumber"], 16)
    val_wei = int(tx["value"], 16)
    val_bnb = val_wei / 1e18
    nonce = int(tx["nonce"], 16)
    print(f"{desc}:")
    print(f"  tx={tx_hash}")
    print(f"  block={blk}, nonce={nonce}, from={tx['from']}, to={tx['to']}, value={val_bnb} BNB, status={rcpt['status']}")
    verified_funders[tx_hash] = {
        "description": desc,
        "blockNumber": blk,
        "nonce": nonce,
        "from": tx["from"],
        "to": tx["to"],
        "valueWei": str(val_wei),
        "valueBNB": val_bnb,
        "status": rcpt["status"],
    }

# Also let's check current nonce, balance, and code of all recipients across Q76, Q78, Q80
with open(r"D:\make_money\flapjax_audit\verified_transfers.json", "r", encoding="utf-8") as f:
    vdata = json.load(f)

all_recipients = sorted({row["recipient"] for day in ("Q76", "Q78", "Q80") for row in vdata[day]})
head_blk = int(rpc_call("eth_blockNumber", []), 16)
print(f"\n=== RECIPIENT LIVE SNAPSHOT AT BLOCK {head_blk} ===")
recipient_states = {}
for addr in all_recipients:
    bal_wei = int(rpc_call("eth_getBalance", [addr, hex(head_blk)]), 16)
    nonce = int(rpc_call("eth_getTransactionCount", [addr, hex(head_blk)]), 16)
    code = rpc_call("eth_getCode", [addr, hex(head_blk)])
    # Also read FLAPJAX balance!
    # balanceOf(address) = 0x70a08231 + 32-byte padded address
    call_data = "0x70a08231" + addr[2:].lower().rjust(64, "0")
    fj_hex = rpc_call("eth_call", [{"to": "0x90c8889f428F9Ebb77BB8f15CAD3a50a9aC680df", "data": call_data}, hex(head_blk)])
    fj_bal = int(fj_hex, 16) // (10**18)
    recipient_states[addr] = {
        "balanceBNB": bal_wei / 1e18,
        "balanceWei": str(bal_wei),
        "nonce": nonce,
        "isContract": code != "0x",
        "balanceFLAPJAX": fj_bal,
    }
    print(f"  {addr}: nonce={nonce}, BNB={bal_wei/1e18:.8f}, contract={code != '0x'}, FLAPJAX={fj_bal:,}")

vdata["verified_funders"] = verified_funders
vdata["recipient_states"] = recipient_states
vdata["snapshot_block"] = head_blk

with open(r"D:\make_money\flapjax_audit\verified_transfers.json", "w", encoding="utf-8") as f:
    json.dump(vdata, f, indent=2)
