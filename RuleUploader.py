class RuleUploader():
	""" Base class used to upload rules to wordpress """
	def upload(self):
		raise NotImplementedError()

	def done(self):
		raise NotImplementedError()
