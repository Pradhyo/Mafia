import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db
from random import randint

template_dir = os.path.join(os.path.dirname(__file__),'www')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

roles = ['Civilian', 'Mafia', 'Doctor', 'Detective']

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
			temp_room = Room(name = room_name, password = room_password, in_progress = False, admin = users.get_current_user().user_id())
			temp_room.put()
			self.response.set_cookie('room', room_name, path='/')
			self.redirect('/#/waiting')		
		else: 
			self.redirect('/')

class CreateUser(Handler):
	def get(self):
		current_room_name = self.request.cookies.get('room')
		current_room = Room.all().filter("name =", current_room_name).get()
		is_admin = current_room.admin == users.get_current_user().user_id()
		if current_room.in_progress:
			self.redirect('#/nightmafia')
		else:
			players = User.all().filter("room =", current_room_name)
			self.render("joined_players.html", players = players, is_admin = is_admin)

	def post(self):
		current_room = self.request.cookies.get('room')
		if current_room:
			username = self.request.get('username')
			current_user = User.all().filter("email =", users.get_current_user().email()).get()
			if username:
				if not current_user:
					temp_user = User(name = username, room = current_room, role = 0, email = users.get_current_user().email(), is_alive = True)
					temp_user.put()
				if current_user:
					current_user.name = username
					current_user.put()
				self.response.set_cookie('user', username, path='/')
				self.redirect('/newuser')					
						
class JoinRoom(Handler):
	def post(self):
		room_name = self.request.get('room_name')
		room_password = self.request.get('room_password')
		
		temp_room = Room.all().filter("name = ", room_name).get()
		if temp_room and temp_room.password == room_password and not temp_room.in_progress:
			self.response.set_cookie('room', room_name, path='/')
			self.redirect('/#/waiting')		
		else: 
			self.redirect('/#/findaroom')	

class GamePlay(Handler):
	def get(self):
		current_room_name = self.request.cookies.get('room')
		current_room = Room.all().filter("name =", current_room_name).get()
		if current_room.in_progress:
			current_user_name = self.request.cookies.get('user')
			mafia = User.all().filter("role =", 1)
			current_user = User.all().filter("name =", current_user_name).get()
			self.response.set_cookie('role', roles[current_user.role], path='/')
			self.render("role.html", role = roles[current_user.role], mafia = mafia)
		else:
			self.redirect('/newuser')

	def post(self):
		current_room_name = self.request.cookies.get('room')
		current_room = Room.all().filter("name =", current_room_name).get()
		players = User.all().filter("room =", current_room_name).fetch(limit=None)
		total_players = len(players)
		if total_players > 3:
			random_user = 0
			while players[random_user].role != 0:
				random_user = randint(0,total_players-1)
			players[random_user].role = 2
			players[random_user].put()
			while players[random_user].role != 0:
				random_user = randint(0,total_players-1)
			players[random_user].role = 3
			players[random_user].put()
			for i in range(total_players/3):
				while players[random_user].role != 0:
					random_user = randint(0,total_players-1)
				players[random_user].role = 1
				players[random_user].put()
			current_room.in_progress = True
			current_room.put()
			self.redirect('/game')
		else:
			self.redirect('/newuser')

class Room(db.Model):
	name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	admin = db.StringProperty(required = True)
	in_progress = db.BooleanProperty(required = True)

class User(db.Model):
	name = db.StringProperty(required = True)
	room = db.StringProperty(required = True)
	email = db.StringProperty(required = True)
	role = db.IntegerProperty()
	is_alive = db.BooleanProperty()
