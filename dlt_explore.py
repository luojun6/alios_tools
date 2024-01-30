import pandas as pd

cpu = "cpu"
date = 'date'
timestamp = 'timestamp'
appid = 'appid'
ctxid = 'ctxid'
level = "level"
payload = 'payload'


cols_normal = [date, timestamp, appid, ctxid, level, payload]
cols_with_cpu = [date, timestamp, cpu, appid, ctxid, level, payload]