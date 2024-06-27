# https://docs.gunicorn.org/en/stable/settings.html
max_requests = 1000
max_requests_jitter = 50

log_file = "-"

bind = "0.0.0.0:3000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = 2
threads = 2
