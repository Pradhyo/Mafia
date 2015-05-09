import webapp2
from handler import MainHandler, CreateUser, JoinRoom, GamePlay, Proceed

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


app = webapp2.WSGIApplication([('/', MainHandler),
							   ('/joinroom', JoinRoom),
							   ('/game', GamePlay),
							   ('/proceed', Proceed),
							   ('/newuser', CreateUser)], 
							   debug=True)

