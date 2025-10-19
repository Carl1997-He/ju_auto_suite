import requests, json
from .yaml_loader import load_yaml
from .logger import get_logger

log = get_logger("feishu")

def send_feishu(content:str, webhook_yaml="config/webhook.yaml"):
    conf = load_yaml(webhook_yaml)
    url = conf.get("feishu",{}).get("webhook_url")
    if not url:
        log.warning("Feishu webhook_url not set. Printing message instead:\n" + content)
        return {"code":-1, "msg":"no webhook", "content": content}
    headers = {"Content-Type":"application/json; charset=utf-8"}
    body = {"msg_type":"text", "content":{"text": content}}
    try:
        r = requests.post(url, headers=headers, data=json.dumps(body), timeout=10)
        log.info(f"Feishu response: {r.status_code} {r.text}")
        return {"code":0, "status": r.status_code}
    except Exception as e:
        log.error(f"Feishu send error: {e}")
        return {"code":-2, "error": str(e)}
