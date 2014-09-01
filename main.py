import webapp2

from google.appengine.ext import db
from google.appengine.api import images

class geopic(db.Model):
	image = db.BlobProperty()
	date = db.StringProperty()

class image_post(webapp2.RequestHandler):
	def post(self):
		newImage = geopic()
		image = images.resize(self.request.get('image'), 640,480)
		
		newImage.image = db.Blob(image)
		
		newImage.get()
		self.response.write(""<meta http-equiv="refresh" content="0.5;URL='/'">"")

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Hello")

		pictures = geopic.gql("ORDER BY date ASC")
		for pic in pictures:
			self.response.write("<img src='/img?photo=%s'>" % pic.key())

class serveImage(webapp2.RequestHandler):
	def get(self):
	pic = db.get(self.request.get('photo'))
	if pic.image:
		self.response.headers['Content-Type'] = 'image/png'
		self.response.out.write(pic.image)

application = webapp2.WSGIApplication([
	('/',MainHandler),
	('/imagepost', image_post),
	('/img', serveImage)
], debug=true)
