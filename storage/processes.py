K_SENT = 'sent'
K_ERRORS = 'errors'
K_UPDATES = 'updates'
K_PROGRESS_VALUE = 'progress_value'	

class ProcessUpdating():
	def __init__(self, name_bot:str, redis_service):
		self.redis_service = redis_service
		self.name_bot = name_bot
		self.status = {
			K_SENT: 0,
			K_ERRORS: 0,
			K_UPDATES: 0,
			K_PROGRESS_VALUE: 0
		}
		try:
			self.load_process()
			if len(self.status) == 0:
				self.set_status(0, 0, 0)
		except:
			self.set_status(0, 0, 0)

		self.status_string = self.__str__()


	def __str__(self):
		self.load_process()
		return f"✅{self.status[K_SENT]} ⚠️{self.status[K_ERRORS]} 🔄{self.status[K_UPDATES]} 📡{self.status[K_PROGRESS_VALUE]}"

	def reset(self):
		self.set_status(0, 0, 0)
		self.save_process()

	def increment_sent(self):
		self.status[K_SENT] += 1
		self.save_process()

	def increment_errors(self):
		self.status[K_ERRORS] += 1	
		self.save_process()

	def set_status(self, sent:int, errors:int, updates:int):
		self.status[K_SENT] = sent
		self.status[K_ERRORS] = errors
		self.status[K_UPDATES] = updates
		try:
			self.status[K_PROGRESS_VALUE] = updates / (sent+errors) * 100
		except ZeroDivisionError:
			self.status[K_PROGRESS_VALUE] = 0
		print(f"set_status: {self.status}")
		self.save_process()

	def save_process(self):
		print(f"save_process: {self.status}")
		self.redis_service.save_process(self)

	def load_process(self):
		self.status = self.redis_service.load_status(self)
		print(f"load_process: {self.status}")

	def delete_process(self):
		self.redis_service.delete_process(self)