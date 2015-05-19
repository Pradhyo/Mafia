import webapp2
from handler import MainHandler, CreateUser, JoinRoom, GamePlay, Proceed, NightVotes, DayVotes, Final

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


app = webapp2.WSGIApplication([('/', MainHandler),
							   ('/joinroom', JoinRoom),
							   ('/game', GamePlay),
							   ('/proceed', Proceed),
							   ('/nightvotes', NightVotes),
							   ('/dayvotes', DayVotes),
							   ('/final', Final),
							   ('/newuser', CreateUser)], 
							   debug=True)


