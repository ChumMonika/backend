import os

# DigitalOcean App Platform uses port 8080 by default
bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
