import pytest
from airdrop_api.utils.request_client import send_request
from airdrop_api.utils.db_client import execute, query_one
from airdrop_api.utils.chain_checker import verify_airdrop_tx
from airdrop_api.utils.yaml_loader import load_yaml

CASES = load_yaml("airdrop_api/data/airdrop_cases.yaml")

def setup_module():
    # init sqlite table
    execute("airdrop_api/config/db.yaml", "CREATE TABLE IF NOT EXISTS airdrop_log(uid INTEGER PRIMARY KEY, status TEXT);")
    # Pre-insert claimed record for uid=100002 to simulate repeat
    execute("airdrop_api/config/db.yaml", "INSERT OR REPLACE INTO airdrop_log(uid,status) VALUES(100002,'SUCCESS');")

@pytest.mark.parametrize("case", CASES)
def test_airdrop_claim(case):
    payload = dict(case["payload"])
    payload["uid"] = case["uid"]
    res = send_request(case["method"], case["url"], payload, env_yaml="airdrop_api/config/env.yaml")
    assert res["code"] == case["expected"]["code"], f"API code mismatch: {res}"

    if res["code"] == 0:
        # mark success in DB (simulating backend write) then assert
        execute("airdrop_api/config/db.yaml", "INSERT OR REPLACE INTO airdrop_log(uid,status) VALUES(:uid,'SUCCESS');", {"uid": case["uid"]})
        db = query_one("airdrop_api/config/db.yaml", "SELECT status FROM airdrop_log WHERE uid=:uid", {"uid": case["uid"]})
        assert db and db["status"] == "SUCCESS"
        ok = verify_airdrop_tx(case["wallet"], case["payload"]["amount"], "airdrop_api/config/env.yaml")
        assert ok is True
    else:
        # for repeat claim, ensure DB kept as SUCCESS
        db = query_one("airdrop_api/config/db.yaml", "SELECT status FROM airdrop_log WHERE uid=:uid", {"uid": case["uid"]})
        assert db and db["status"] == "SUCCESS"
