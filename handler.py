import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db

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

	def post(self):
		room_name = self.request.get('room_name')
		room_password = self.request.get('room_password')
		
		if room_password and room_name:
			temp_room = Room(name = room_name, password = room_password)
			temp_room.put()
			self.response.set_cookie('room', room_name, max_age=360, path='/')
			self.redirect('/#/waiting')		
		else: 
			self.redirect('/')

class CreateUser(Handler):
	def post(self):
		current_room = self.request.cookies.get('room')
		if current_room:
			username = self.request.get('username')
			if username:
				temp_user = User(name = username, room = current_room)
				temp_user.put()
				self.response.set_cookie('user', username, max_age=360, path='/')
				self.redirect('/#/nightmafia')
		
class JoinRoom(Handler):
	def post(self):
		room_name = self.request.get('room_name')
		room_password = self.request.get('room_password')
		
		temp_room = Room.all()
		temp_room.filter("name = ", room_name)
		temp_room.filter("password = ", room_password)
		temp_room = temp_room.fetch(1)
		if temp_room:
			self.response.set_cookie('room', room_name, max_age=360, path='/')
			self.redirect('/#/waiting')		
		else: 
			self.redirect('/#/findaroom')	


class Room(db.Model):
	name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	admin = db.UserProperty(auto_current_user_add = True)

class User(db.Model):
	name = db.StringProperty(required = True)
	room = db.StringProperty(required = True)
	role = db.IntegerProperty()
	is_alive = db.BooleanProperty()
