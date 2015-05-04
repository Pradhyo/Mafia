import webapp2
from handler import MainHandler, CreateUser, JoinRoom, GamePlay

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


app = webapp2.WSGIApplication([('/', MainHandler),
							   ('/joinroom', JoinRoom),
							   ('/game', GamePlay),
							   ('/newuser', CreateUser)], 
							   debug=True)
