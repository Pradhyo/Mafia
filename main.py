import webapp2
from handler import MainHandler

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
