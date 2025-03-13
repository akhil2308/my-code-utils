import json
import logging
from datetime import datetime, timedelta

from celery import Celery
from celery.beat import Scheduler, ScheduleEntry, Service
from celery.schedules import schedule, crontab

from sqlalchemy import create_engine, Column, String, Integer, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from croniter import croniter

# Configure logging
logging.basicConfig(level=logging.INFO)

# -------------------------------
# SQLAlchemy Setup
# -------------------------------
Base = declarative_base()

class ScheduledTask(Base):
    __tablename__ = 'scheduled_tasks'
    
    id = Column(Integer, primary_key=True)
    scheduler_type = Column(String, nullable=False, default='interval')
    # For interval type, store a JSON like {"days": 0, "hours": 20, "minutes": 0, "seconds": 0}
    # For crontab type, store a JSON like {"minute": "0", "hour": "20", "day_of_week": "*", "day_of_month": "*", "month_of_year": "*"}
    schedule_params = Column(JSON, nullable=False)
    task_function = Column(String, nullable=False)
    args = Column(JSON, nullable=True)

# Connect to your PostgreSQL database.
engine = create_engine('postgresql+psycopg2://postgres:@localhost:5432/test')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# -------------------------------
# Custom Scheduler Definition
# -------------------------------
class SQLAlchemyScheduler(Scheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        """
        Example Scenarios
            First Run:

                self._last_sync is None.

                should_sync() returns True (immediate sync).

            Periodic Sync:

                sync_every = 300 (sync every 5 minutes).

                If time.monotonic() - self._last_sync > 300, should_sync() returns True.

            Task-Based Sync:

                sync_every_tasks = 10 (sync after 10 tasks).

                If self._tasks_since_sync >= 10, should_sync() returns True.

            Combined Sync:

                sync_every = 300 and sync_every_tasks = 10.

                Syncs every 5 minutes or after 10 tasks, whichever comes first.
        """ 
        #: How often to sync the schedule (3 minutes by default)
        self.sync_every = 30
        #: How many tasks can be called before a sync is forced.
        # sync_every_tasks = None
        logging.info("SQLAlchemyScheduler initialized.")

    def sync(self):
        logging.info("Syncing schedule with database...")
        session = Session()
        try:
            db_tasks = session.query(ScheduledTask).all()
            current_ids = {task.id for task in db_tasks}
            logging.info("Found %d task(s) in DB", len(db_tasks))

            # Remove schedule entries that no longer exist in the DB.
            for entry_name in list(self.schedule.keys()):
                try:
                    task_id = int(entry_name.split('_')[-1])
                except ValueError:
                    task_id = None
                if task_id not in current_ids:
                    self.schedule.pop(entry_name, None)
                    logging.info("Removed schedule entry: %s (not in DB)", entry_name)

            # Process each task from the DB.
            for task in db_tasks:
                entry_name = f"{task.task_function}_{task.id}"
                logging.info("Processing task: %s with scheduler type: %s", entry_name, task.scheduler_type)

                if task.scheduler_type == 'interval':
                    # For interval, schedule_params should be a dict with keys matching timedelta arguments.
                    try:
                        delta = timedelta(**task.schedule_params)
                    except Exception as e:
                        logging.error("Error parsing interval schedule_params for task %s: %s", entry_name, e)
                        continue
                    sched = schedule(delta)
                    logging.info("Interval schedule for %s set to %s", entry_name, delta)
                elif task.scheduler_type == 'crontab':
                    # For crontab, schedule_params is passed directly to crontab.
                    try:
                        sched = crontab(**task.schedule_params)
                    except Exception as e:
                        logging.error("Error parsing crontab schedule_params for task %s: %s", entry_name, e)
                        continue
                    logging.info("Crontab schedule for %s set with parameters %s", entry_name, task.schedule_params)
                else:
                    logging.error("Unknown scheduler type for task %s: %s", entry_name, task.scheduler_type)
                    continue

                task_args = task.args if task.args is not None else ()

                if entry_name not in self.schedule: 
                    self.schedule[entry_name] = ScheduleEntry(
                        name=entry_name,
                        task=task.task_function,
                        schedule=sched,
                        args=task_args,
                        kwargs={},
                        options={},
                        last_run_at=None,
                    )
                    logging.info(f"Added new schedule entry: {entry_name}")
                else:
                    entry = self.schedule[entry_name]
                    entry.schedule = sched
                    entry.args = task_args
                    logging.info("Updated schedule entry: %s", entry_name)
            
        finally:
            session.close()

        return self.schedule




# -------------------------------
# Celery App Setup
# -------------------------------
app = Celery(
    'test_app',
    broker='redis://localhost:6379/0',
    backend='db+postgresql+psycopg2://postgres:@localhost:5432/test'
)
# app.conf.CELERY_TIMEZONE = 'Asia/Kolkata'
app.conf.enable_utc = False # Disable UTC for easier debugging.

if __name__ == '__main__':
    beat_service = Service(app=app, scheduler_cls=SQLAlchemyScheduler)
    beat_service.start()
    # celery -A test_app beat --loglevel=info --scheduler=sqlalchemy_scheduler.SQLAlchemyScheduler --max-interval=10
