from pg import pg
from crawler import Crawler
from timekeeper import TimeKeeper
import time
class Manager:
	def addUser(self, user, pw):
		if self.dim == 1:
			self.user = [self.user, user]
			self.pw = [self.pw, pw]
			self.sql = [self.sql, pg(user,"db-user","db-passwd")]
			self.dim = 2
		else:
			self.user.append(user)
			self.pw.append(pw)
			self.sql.append(pg(user,"db-user","db-passwd"))
			self.dim += 1
	def __init__(self, user, pw):
		self.user = user
		self.pw = pw
		self.sql = pg(user,"db-user","db-passwd")
		self.tk = TimeKeeper()
		self.crawler = Crawler(user, pw, self.sql);
		self.indx = 0
		self.dim = 1
	def HourlyLikes(self):
		likes = int(self.sql[self.indx].HourlyLikes())
		return likes
	def run(self, num):
		self.indx = num
		likes = self.HourlyLikes()
		if(likes >= 300):
			print("Already liked 300 pages in the last hr, going to next")
			self.indx += 1	
			if(self.indx >= self.dim):
				self.indx = 0		
			self.run(self.indx)
		else:
			quota = 300-likes
			print("Initiating crawler")
			if self.crawler.login(self.user[num],self.pw[num],self.sql[num]):
				self.indx += 1
				if(self.indx >= self.dim): self.indx = 0
				self.crawler.login(self.user[self.indx],self.pw[self.indx],self.sql[self.indx])
			posts = self.getFreshLinks()
			posts = posts[0:quota]
			print(posts)
			print(quota)
			
			self.crawler.likeLinks(posts)
		#	self.crawler.exit()
			self.run(self.indx)
	def runTags(self, tags):
		likes = self.HourlyLikes()
		if(likes >= 300):
			print("Already liked 300 pages in the last hr, will check again in 20 minutes")
			time.sleep(20*60)
			self.runTags(tags)
		else:
			quota = 300-likes
			print("Initiating crawler")
			self.crawler.login()
			posts = self.getLinksFromTags(tags)
			posts = posts[0:quota]
			print(posts)
			print(quota)
			
			self.crawler.likeLinks(posts)
			self.crawler.exit()
			self.runTags(tags)
	def newTags(self, tags):
		for tag in tags:
			self.sql[self.indx].addTag(tag)
	#also shows if tag exists if tag time is False
	def getSnaps(self,tags, num):
		self.crawler.login()
		links = self.crawler.LinksFromTagsIter(tags,num)
		snaps = self.crawler.checkSnaps(links)
	def getTagTimes(self, tags):
		tags_times = []
		for tag in tags:
			time = self.sql[self.indx].getTagTime(tag)
			tags_times.append([tag,time])
		return tags_times
	def getAllTagsTimes(self):
		tags = self.sql[self.indx].getAllTagsTimes()
		return(tags)
	def getFreshTags(self):
		tagstimes = self.getAllTagsTimes()
		tagstimes_fresh = self.tk.FreshTags(tagstimes, 5) #5 tags at a time
		tags = []
		for tagtime in tagstimes_fresh:
			tag = tagtime[0]
			tags.append(tag)
		return tags
	def getFreshTagNum(self,num):
		tagstimes = self.getAllTagsTimes()
		tagstimes_fresh = self.tk.FreshTags(tagstimes, num) #1 tag at a time
		tags = []
		for tagtime in tagstimes_fresh:
			tag = tagtime[0]
			tags.append(tag)
		return tags
	def getLinksFromTags(self,tags):
		links = self.crawler.searchTagList(tags)
		return links
	def getFreshLinks(self):
		tags = self.getFreshTags()
		self.newTags(tags)
		links = self.getLinksFromTags(tags)
		return links
	def getFreshLinksNTags(self, n):
		tags = self.getFreshTagNum(n)
		self.newTags(tags)
		links = self.getLinksFromTags(tags)
		return links
	def getHashTagsFromLink(self,link):
		self.crawler.login()
		self.crawler.getHashTagsFromLink(link)
		self.crawler.exit()
	def getFreshHashTags(self):
		self.crawler.login()
		links = self.getFreshLinksNTags(50)
		tags = []
		for link in links:
			_tags = self.crawler.getHashTagsFromLink(link)
			tags.extend(_tags)	
		import collections
		counter = collections.Counter(tags)
		print(counter.most_common(10))
		self.crawler.exit()
		return tags
