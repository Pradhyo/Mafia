import webapp2
import jinja2
import os
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__),'www')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self,template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

class MainHandler(Handler):
	def get(self):
		# Checks for active Google account session
		user = users.get_current_user()

		if user:
			self.render("index.html", name = user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))


