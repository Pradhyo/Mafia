import webapp2
from handler import MainHandler, CreateUser

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


app = webapp2.WSGIApplication([('/', MainHandler),
							   ('/newuser', CreateUser)], 
							   debug=True)
