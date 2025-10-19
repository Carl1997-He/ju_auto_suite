from feishu_notifier.utils.feishu_sender import send_feishu
from feishu_notifier.utils.log_parser import extract_summary

def push_daily_report():
    summary = extract_summary("feishu_notifier/logs/pytest_run.log")
    content = f"📊 接口自动化执行日报\n{summary}"
    send_feishu(content, "feishu_notifier/config/webhook.yaml")

if __name__ == "__main__":
    push_daily_report()
