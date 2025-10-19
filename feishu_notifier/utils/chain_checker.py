from .yaml_loader import load_yaml
from .logger import get_logger

log = get_logger("chain_checker")

def verify_airdrop_tx(wallet:str, expected_amount:float, chain_yaml="config/env.yaml")->bool:
    # In MOCK mode returns True if expected_amount > 0 and wallet starts with '0x'.
    env = load_yaml(chain_yaml)
    if env.get("MOCK", True):
        ok = str(wallet).startswith("0x") and (float(expected_amount) > 0)
        log.info(f"[MOCK] chain verify wallet={wallet} amount={expected_amount} -> {ok}")
        return ok
    # Real web3 verification could be added here when RPC/contract is provided.
    return True

def get_ju_transfers(wallet:str, chain_yaml="config/env.yaml"):
    env = load_yaml(chain_yaml)
    if env.get("MOCK", True):
        # Return a list of dicts like actual transfers
        return [{"token":"JU","value":120},{"token":"JU","value":60},{"token":"USDT","value":5}]
    return []
