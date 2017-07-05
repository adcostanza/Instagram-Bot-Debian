import datetime
class TimeKeeper:
	def __init__(self):
		self.go = False
	def FreshTags(self, tags_times, num):
		tags_secs = []
		for tag_time in tags_times:
			tag = tag_time[0]
			time = tag_time[1]
			sec = (datetime.datetime.now()-time).total_seconds()
			tag_sec = [tag, sec]
			tags_secs.append(tag_sec)
		tags_secs = sorted(tags_secs,key=lambda x: x[1], reverse=True)
		tags_secs = tags_secs[0:num]
		return(tags_secs)