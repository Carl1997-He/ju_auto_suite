from jugame_reward_check.utils.request_client import send_request
from jugame_reward_check.utils.db_client import execute, query_one
from jugame_reward_check.utils.chain_checker import get_ju_transfers
from jugame_reward_check.utils.feishu_sender import send_feishu
from jugame_reward_check.utils.yaml_loader import load_yaml

def compare_rewards_for_uid(uid:int, wallet:str, expected:int)->tuple[bool,str]:
    # Simulate API returns amount per uid
    api = send_request("GET", "/game/reward", params={"uid": uid}, env_yaml="jugame_reward_check/config/env.yaml")
    api_amount = api.get("amount", 0)

    # DB expected record (simulate it mirrors api when correct)
    row = query_one("jugame_reward_check/config/db.yaml", "SELECT expected FROM exp_reward WHERE uid=:uid", {"uid":uid})
    db_expect = row["expected"] if row else None

    # Chain aggregation in mock
    txs = get_ju_transfers(wallet, "jugame_reward_check/config/env.yaml")
    chain_amount = sum(t["value"] for t in txs if t["token"] == "JU" )

    ok_api = (api_amount == expected)
    ok_db  = (db_expect == expected) if db_expect is not None else True
    ok_chain = (chain_amount >= expected)  # allow >= to account for cumulative transfers in mock

    problems = []
    if not ok_api: problems.append(f"API {api_amount} != expected {expected}")
    if not ok_db: problems.append(f"DB {db_expect} != expected {expected}")
    if not ok_chain: problems.append(f"Chain {chain_amount} < expected {expected}")
    return (len(problems)==0, "; ".join(problems))

def process_all_players():
    players = load_yaml("jugame_reward_check/data/players.yaml")
    # bootstrap DB table
    execute("jugame_reward_check/config/db.yaml", "CREATE TABLE IF NOT EXISTS exp_reward(uid INTEGER PRIMARY KEY, expected INTEGER);")
    for p in players:
        execute("jugame_reward_check/config/db.yaml", "INSERT OR REPLACE INTO exp_reward(uid, expected) VALUES(:uid, :expected)", {"uid":p["uid"], "expected": p["expected_reward"]})
        ok, msg = compare_rewards_for_uid(p["uid"], p["wallet"], p["expected_reward"])
        if not ok:
            send_feishu(f"⚠️ Reward mismatch for uid={p['uid']}: {msg}", "jugame_reward_check/config/webhook.yaml")

if __name__ == "__main__":
    process_all_players()
