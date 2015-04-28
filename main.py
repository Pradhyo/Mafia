import webapp2
from handler import MainHandler, CreateUser, JoinRoom

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


app = webapp2.WSGIApplication([('/', MainHandler),
							   ('/joinroom', JoinRoom),
							   ('/newuser', CreateUser)], 
							   debug=True)
