import webapp2


class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Hello, webapp2 World! la la la ')


app = webapp2.WSGIApplication([('/helloworld', MainPage)],
				debug=True)
