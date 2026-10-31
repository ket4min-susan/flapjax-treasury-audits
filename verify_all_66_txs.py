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

TREASURY = "0x7c34e9e21ee28a49ff0b84b61774119e6633359f"
TOKEN = "0x90c8889f428f9ebb77bb8f15cad3a50a9ac680df"
TRANSFER_SIG = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

q76_txs = [
    "0xf7aa9f0af86d61fb7f622c0b23e303ef8e81c69bd32f117c8d03ffaaf5c3446f",
    "0xb7ddb8d2148c86df17c74c365c157988c29223db94e5589c401ce154f69b66ac",
    "0xe3361cbd6e9d5790fccb387817b5a510120f2e929c2044377e817ac48ac78509",
    "0xe39fc522129401b61b2c054a6547627616d7f6bc95cf8f9daba39d605f6059d1",
    "0xfedc430f0ad96869a0b1bee7f58948386ba829f9a9f89884919d0f61ce1e0b17",
    "0xbf53b76946623314f4e5c86c1e266c32f7dc321d36742d4ae7733e353c80a8c8",
    "0x0be8025307dfd9172187c323f0092bacf1f34948ae15e4df44558ddf65b03156",
    "0xb6b4c1b363e9ca0f78740d828f05af0bd991964ab229b60f7e3a144ce5533e3a",
    "0xdbbc176086c918fa790c648eba56e773fbee0a14882d862b9e0b7bcb5304c2f0",
    "0x95b98673fd1328486b31a9bedc677e7ca8c48fed9d03511328cbbd50b9ec86a7",
    "0x4af89a6778cf16f5a60ac472fda31c38d8c1e5c53fa0a1487505ec77d6daf862",
    "0x0a8289e71d4f4d81d214aa41c40eea4eaa1bf2d0095e7c5e16f9795b7b3e429a",
    "0xbefc7b770b605ba2b378a21062a4e2c99f779b70fbb76643b7a3f468ad325fc1",
    "0xd4e345a7e3277cd337c782ec8add908d7c1746a28b924139e7d73bed8f43cbaa",
    "0xd105ffcc87cd6a562e6cc40da6e47c2a3c32407d10f3f2e98dc8260f4bfd8efa",
    "0xd49f035045ce1cd1b86ed70ab103829e3dabacd844d626752a4a6ba833451bc3",
    "0xc791c561ee5d5950603e2065e354c4aaeb858ec858d5518b281f575a65a16955",
    "0x83a1dcfd052e5b1df8ef0cb82f380a9cd7b6c90f3a947f2ae412a95cfc9b0257",
    "0x04f18370dca64be04e52bc70981b3d48d7cefe584684e0efb724f5c4de376bb2",
    "0xd0ebd47189d241075d29bee65dd8860417ae3623441e391ccb8d83ed6c2a12ea",
    "0x5c38c93ea8462d81af634c8a349adc517b3d2191173bea3d73f07a9fe620b1b1",
    "0xd4d0a4d92a71bd810690f2a758017df44d3d3e8adfaa0a0fbb32a098f7edcb04",
    "0x359244a3a9c52b001534c27475842d62decd28d518e4bebfd743633427363135",
    "0x6838b1888ca60ed954f7e66a44ed29a6f399a7e3dbb906a7f2bece6abbdbb801",
    "0xfb2ab1699e1e6eea073ac7227a4bc4d1bbde9e29a368e9acb85c5a982f736d07",
    "0x81616b3e0787f5d2a35e02ee17814a29cd169712f8e2bae6bbf72a467a73d314",
    "0x5720a2eb63405265998d12a141d353f7b3ba22a9a05eea70c9003b9cf916697b",
    "0xb9ba419f2a1985711ce2a2a3fd2b408d9884ddba375cb9298cf21945285ff220",
    "0x8f1375d552091f7690b1509058544db03f4bc5c43524e635389168e0e953e0d7",
    "0x40806f42cbe62411170e18861dc4092a68dc7608c688df6939f5b07a9a3bb161",
    "0xae1afa315c1741ff91309f0445b17a0da994bfc5844e4909ed5d9546b1d0d54b",
]

q78_txs = [
    "0xbfc21c7712f9ac9a4169e211e0e341d14236fbc097fae2e03852cce1ef0e7952",
    "0x76f4abaa6a14005726257d1412d9a9842af6c09a5bb6395c2604f844f9bff77d",
    "0xdd2feb71c1dda3945b233ab7c924b1d1e6d52b7d3dcd4cc6354e3248df9b3da4",
    "0x8c6305282436e1867eeac42b859ff947dad7f0db447af34fb8ff7185d88bb0d9",
    "0xe468d224801e50cf936296a8f79b6bc9dc13d14bede24bd9945312e597b2074e",
    "0x7e8f90f49597397529cc81cea8723debc2dd08da35ba78999fcc2840dc4cad0c",
    "0x0c7d758ba9955a141839d137c2830b41860eb00ccdb0bb1a10ef33829e9b1bb6",
    "0x825b5c67d1cf033e9f756dcd5c69f683d77f2478ee0ee5d8f6b04d42df05c8ae",
    "0x388a55851ce63aaf984e6671f305155b165c47225dc5d7dab0e47d8ce2763372",
    "0x69fea445443ca8d27e43d3c11f53aaa34a2edc7e997e84668409d86eb021abb5",
    "0x3f4d252efc70064dd841e062847aad926bebca630137787832c77b10fd246de5",
    "0x4f591ad86bb514247d59dbc91cf5793b0a63f22b9e73929aa4bb05946cc3f1f9",
    "0x00b7423c3baf0986ceda24d5286733747a5aed181106a8cf166f6319eacd94bd",
    "0x41f5bc43f9d147a414d86778cfee19c21b62da0d8fed1f9e22cd04f36b283c8e",
    "0x36485b4966c1dbcd0198d840a865c4e97e2fec32c5f1f74cf55f5030d88bae37",
    "0x9af6e7e8ba53540a930d3a7c532af1637c6ccc6324067ab402693b24aff992b0",
    "0xcdbada2d2795f663a10fdb373337139f93b11256a6dfe102368c4538149412a5",
]

q80_txs = [
    "0x44a580d841831667955ea9e7bfcb75521ccc51c5b2ffc7299ef70bbb50fa78d5",
    "0x6895a4d32f4367704230435d86202b048a06c2f9d3c452fc21419ca1e5a2dac5",
    "0xce38980fb1f4add7ab7dc6cf739001ded5bfac0d80756e915a4ba48d0d40b292",
    "0x30a82d0d9c77d6dac96e6595cd4557845cd8695fb099d93fb54b5982e221ca02",
    "0x58e92d0c8afedb71ca5b98e0810dc1856f1406e81b7fbe0f8bbab6c6ed8174b6",
    "0x81083d6b118a34358abdf3d1289ed469ca3af4871677043837d5d055c0e90e03",
    "0x9e9358acf04da74162ba29333e988fe6f323256d9287c37d2ea06e8bbcfa2dd3",
    "0x18324f74d9afbe0a7517cfc7c1c342f386817c71202bad7fa294ef05f83743e1",
    "0x875c2ef38cdd206ebd49735f5cfd5755bcd5fc85cb60c78e073153953cd60550",
    "0xc1eac754961dc07ecc103c831197f039b23588924ff0d56efccdb1ece523b11e",
    "0x15e20669d88b516a43a8fafffbf2f6579ea43f15af1139e48550bef16569be46",
    "0x3ee7dff7623561a6ee06f3a599ef6025a44c28fd85855398e6acfc25565968b2",
    "0xf066f28c0de3964e4dc06e2481a468c53fd221f962905b922078d9efae154cbd",
    "0x664cfae4cd1553557c05a31c5e3fbc662afb2472f3d93df461f9b4f6f0bc7bc4",
    "0x814720410be30518ea1947c13b283b4dbe408a35c82f05f89fe00b07a4d14d1a",
    "0xfb6c7f0f5edf392be0b71da8561c01b2ef111b82e40d628b2d2b7173417efb85",
    "0x1ff5c6086cc2f3960c0e1460f0482e5af5f9c059d091bfcd1f2ac888c88401b1",
    "0x4c9170b0bab813ff1d43e8d200a3df72eb661a6446959a8485746ba2688d62bf",
]

cot_tz = timezone(timedelta(hours=-5))

def verify_tx_list(name, tx_list):
    out = []
    total_wei = 0
    recipients = set()
    for tx_hash in tx_list:
        rcpt = rpc_call("eth_getTransactionReceipt", [tx_hash])
        tx_obj = rpc_call("eth_getTransactionByHash", [tx_hash])
        assert rcpt["status"] == "0x1", f"Failed tx {tx_hash}"
        blk_num = int(rcpt["blockNumber"], 16)
        # get timestamp from log or block
        ts = None
        transfer_logs = [
            l for l in rcpt["logs"]
            if l["address"].lower() == TOKEN
            and len(l["topics"]) >= 3
            and l["topics"][0].lower() == TRANSFER_SIG
            and ("0x" + l["topics"][1][-40:]).lower() == TREASURY
        ]
        assert len(transfer_logs) == 1, f"Expected 1 transfer log in {tx_hash}"
        tlog = transfer_logs[0]
        if "blockTimestamp" in tlog:
            ts = int(tlog["blockTimestamp"], 16)
        else:
            blk = rpc_call("eth_getBlockByNumber", [hex(blk_num), False])
            ts = int(blk["timestamp"], 16)
        recipient = "0x" + tlog["topics"][2][-40:]
        amount_wei = int(tlog["data"], 16)
        amount_fj = amount_wei // (10**18)
        total_wei += amount_wei
        recipients.add(recipient.lower())
        dt_cot = datetime.fromtimestamp(ts, tz=cot_tz).strftime("%Y-%m-%d %H:%M:%S")
        dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        out.append({
            "txHash": tx_hash,
            "nonce": int(tx_obj["nonce"], 16),
            "blockNumber": blk_num,
            "timestamp": ts,
            "timeCOT": dt_cot,
            "timeUTC": dt_utc,
            "recipient": recipient,
            "amountWei": str(amount_wei),
            "amountFLAPJAX": amount_fj,
        })
    # Check nonces!
    nonces = [x["nonce"] for x in out]
    print(f"=== {name} ===")
    print(f"Count: {len(out)}, Total FLAPJAX: {total_wei // (10**18):,}, Distinct Recipients: {len(recipients)}")
    print(f"Nonces: {min(nonces)}..{max(nonces)} (contiguous={nonces == list(range(min(nonces), max(nonces)+1))})")
    if nonces != list(range(min(nonces), max(nonces)+1)):
        missing = set(range(min(nonces), max(nonces)+1)) - set(nonces)
        print(f"  Missing nonces in {name}: {sorted(missing)}")
    return out

res_q76 = verify_tx_list("Q76 (2026-10-27 COT)", q76_txs)
res_q78 = verify_tx_list("Q78 (2026-10-28 COT)", q78_txs)
res_q80 = verify_tx_list("Q80 (2026-10-29 COT)", q80_txs)

with open(r"D:\make_money\flapjax_audit\verified_transfers.json", "w", encoding="utf-8") as f:
    json.dump({"Q76": res_q76, "Q78": res_q78, "Q80": res_q80}, f, indent=2)
