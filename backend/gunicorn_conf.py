import multiprocessing, os

bind = "0.0.0.0:8000"
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
errorlog  = "-"
