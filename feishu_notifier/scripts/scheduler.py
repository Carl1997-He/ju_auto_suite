from apscheduler.schedulers.blocking import BlockingScheduler
from feishu_notifier.scripts.daily_report import push_daily_report

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(push_daily_report, 'cron', hour=10)  # 每天 10:00
    print("Feishu notifier scheduler started (daily 10:00). Ctrl+C to stop.")
    scheduler.start()

if __name__ == "__main__":
    main()
