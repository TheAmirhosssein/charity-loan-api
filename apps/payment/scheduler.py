from apscheduler.schedulers.background import BackgroundScheduler
from apps.payment.tasks import automatic_payment


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(automatic_payment, trigger="cron", hour=0, minute=1)
    scheduler.start()
