workers = 2
threads = 2
wsgi_app = "WebHost:get_app()"
accesslog = "-"
access_log_format = (
    '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
worker_class = "gthread"  # "sync" | "gthread"
forwarded_allow_ips = "*"
loglevel = "info"

"""
You can programatically set values.
For example, set number of workers to half of the cpu count:

import multiprocessing

workers = multiprocessing.cpu_count() / 2
"""
