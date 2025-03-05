from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from asyncio import run
import logging

# Configure logging for the application
logging.basicConfig(level=logging.INFO)

# Define an asynchronous function to perform cleanup tasks
async def cleanup_workers():
    try:
        # Replace this print with actual cleanup logic
        print("Cleaning up workers")
    except Exception as e:
        # Log the error instead of printing to stdout
        logging.error(f"Failed to cleanup workers: {e}")

# Initialize the APScheduler BackgroundScheduler
# Note: For production, consider a persistent job store if needed.
scheduler = BackgroundScheduler()

# Create the FastAPI application
app = FastAPI()

# Startup event: Initialize and start the scheduler
@app.on_event("startup")
async def start_scheduler():
    logging.info("Starting scheduler")
    # Add a job that runs every minute (using cron syntax)
    # Using a lambda to run the async cleanup_workers() function via asyncio.run()
    # Alternatively, you could use an async executor or schedule a background task if appropriate.
    scheduler.add_job(lambda: run(cleanup_workers()), CronTrigger(minute="*/1"))
    scheduler.start()

# Shutdown event: Cleanly shutdown the scheduler when the app stops
@app.on_event("shutdown")
async def shutdown_scheduler():
    logging.info("Shutting down scheduler")
    scheduler.shutdown()

# Entry point for running the application
if __name__ == "__main__":
    import uvicorn
    # In production, you might deploy using a process manager (like Gunicorn with UvicornWorker)
    # Here reload is disabled for production readiness.
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
