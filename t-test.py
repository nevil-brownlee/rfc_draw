import time, datetime

t = datetime.datetime.now()
print("start t %s" % t)

t2 = datetime.datetime.now()
tqq = datetime.timedelta.total_seconds(t2-t)
print("t2-t = %s" % tqq)

