from celery import Celery

app = Celery('test_app',
             broker='redis://localhost:6379/0',
             backend='db+postgresql+psycopg2://postgres:@localhost:5432/test')


@app.task(name="send_email")
def send_email(args):
    print(f"Sending email: {args}")
