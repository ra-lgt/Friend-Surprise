from datetime import datetime, timedelta

now = datetime.now()
midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)
print((midnight - now).total_seconds())