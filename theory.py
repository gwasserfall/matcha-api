class Test():
	def __init__(self):
		print "asd"

	def many(self):
		r = []
		for i in range(10):
			r.append(Test())
		print r

t = Test()

t.many()