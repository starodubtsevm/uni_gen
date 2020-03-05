
#---------------------------------------
class comparator(object):

	def __init__(self, threshold_min,threshold_max, delay):
		"""initialization"""
		self.thres_min = threshold_min
		self.thres_max = threshold_max
		self.prev = 0
		tick = 1.0/16000
		self.delay = (delay * 1e-2)/tick
		self.delay_count = 0


	def proc(self, sample):
		"""comparing"""
		if self.delay_count > 0:
			self.delay_count -= 1
			return self.prev
		else:
			if sample >= self.thres_max:
				self.prev = 1
				self.delay_count = self.delay
				return 1

			else:
			    #if sample <= self.thres_min:
				self.prev = 0
				self.delay_count = self.delay
				return 0

