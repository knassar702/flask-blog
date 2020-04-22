from datetime import datetime

def date():
	now = datetime.today()
	date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
	return date

