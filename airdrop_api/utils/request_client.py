import os, time, random
import requests
from .yaml_loader import load_yaml
from .logger import get_logger

log = get_logger("request_client")

class RequestClient:
    def __init__(self, env_yaml:str):
        env = load_yaml(env_yaml)
        self.base_url = env.get("BASE_URL", "http://localhost:18080")
        self.timeout = env.get("TIMEOUT", 10)
        self.mock = env.get("MOCK", True)
        self.latency_ms = env.get("MOCK_LATENCY_MS", [50, 120])
        self.headers = env.get("HEADERS", {"Content-Type": "application/json"})
        self.tokens = env.get("TOKENS", {})
        self.env = env

    def _simulate_latency(self):
        lo, hi = self.latency_ms if isinstance(self.latency_ms, list) else (0, 0)
        time.sleep(random.uniform(lo/1000, hi/1000))

    def _mock_response(self, method, url, json=None, params=None):
        # Basic route-based mocking for demo
        full = f"{self.base_url}{url}"
        log.info(f"[MOCK] {method} {full} json={json} params={params}")
        self._simulate_latency()
        # Airdrop claim mock
        if "/api/airdrop/claim" in url and method.upper() == "POST":
            uid = (json or {}).get("uid")
            activity_id = (json or {}).get("activity_id")
            if uid in (100002,):  # already claimed
                return {"code": 4001, "msg": "already claimed"}
            return {"code": 0, "msg": "success", "activity_id": activity_id}
        # JuGame reward query mock
        if "/game/reward" in url and method.upper() == "GET":
            uid = int(params.get("uid"))
            mapping = {200101:120, 200102:60, 200103:90}
            return {"code":0, "uid":uid, "amount": mapping.get(uid, 0)}
        return {"code": 0, "msg": "ok"}

    def request(self, method:str, url:str, *, json=None, params=None, headers=None):
        if self.mock:
            return self._mock_response(method, url, json=json, params=params)
        full = f"{self.base_url}{url}"
        hdrs = self.headers.copy()
        if headers:
            hdrs.update(headers)
        log.info(f"{method} {full}")
        resp = requests.request(method, full, json=json, params=params, headers=hdrs, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

def send_request(method, url, payload=None, params=None, env_yaml="config/env.yaml"):
    client = RequestClient(env_yaml)
    if method.upper() in ("POST","PUT","PATCH"):
        return client.request(method, url, json=payload, params=params)
    return client.request(method, url, params=params)
