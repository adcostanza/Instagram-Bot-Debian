class tagSplitter:
	def __init__(self, tags):
		self.tags = tags
		
	def sp(self, n):
		l=self.tags
		split = [l[i:i + n] for i in range(0, len(l), n)]
		return(split)
