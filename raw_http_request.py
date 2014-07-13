def get_request_data(url, data=None, headers={}, **kwargs):
	import io
	buffer = io.BytesIO()
	buffer.sendall = buffer.write

	targets = [httplib.HTTPConnection,httplib.HTTPSConnection]
	old_connects = [target.connect for target in targets]

	def fake_connect(self, buffer): self.sock = buffer
	for target in targets: target.connect = lambda self:fake_connect(self,buffer)
	try:
		urllib2.urlopen(urllib2.Request(url, data=data, headers=headers, **kwargs)).read()
	except AttributeError:  # socket interface only partially implemented on StringIO
		pass # missing makefile method throws an AttributeError in HTTPResponse.__init__
	finally:
		for i,target in enumerate(targets): target.connect = old_connects[i]
	return buffer.getvalue()
