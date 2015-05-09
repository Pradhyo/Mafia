import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db
from random import randint, sample

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
			temp_room = Room(name = room_name, password = room_password, in_progress = False, admin = users.get_current_user().user_id(), is_day = None)
			temp_room.put()
			self.response.set_cookie('room', room_name, path='/')
			self.response.set_cookie('room_admin', 'True', path='/')			
			self.redirect('/#/waiting')		
		else: 
			self.redirect('/')

class CreateUser(Handler):
	def get(self):
		current_room_name = self.request.cookies.get('room')
		current_room = Room.all().filter("name =", current_room_name).get()
		is_admin = current_room.admin == users.get_current_user().user_id()
		if current_room.in_progress:
			self.redirect('/game')
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
					temp_user = User(name = username, room = current_room, role = 0, email = users.get_current_user().email(), is_alive = True, vote = "")
					temp_user.put()
				if current_user:
					current_user.name = username
					current_user.room = current_room
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
		mafias = User.all().filter("room =", current_room_name).filter("role =", 1).filter("is_alive =", True).count()
		civilians = User.all().filter("room =", current_room_name).filter("role =", 0).filter("is_alive =", True).count()

		if current_room.in_progress:
			if current_room.is_day == None:
				current_user_name = self.request.cookies.get('user')
				mafia = User.all().filter("room =", current_room_name).filter("role =", 1)
				current_user = User.all().filter("name =", current_user_name).get()
				self.response.set_cookie('role', roles[current_user.role], path='/')
				is_admin = self.request.cookies.get('room_admin')
				self.render("role.html", role = roles[current_user.role], mafia = mafia, is_admin = is_admin)
			elif mafias >= civilians:
				self.write('Mafia win')
			elif mafias == 0:
				self.write('Civilians win')
			elif current_room.is_day == False:
				players = User.all().filter("room =", current_room_name)
				current_role = self.request.cookies.get('role')
				self.render("night.html", players = players, current_role = current_role, hanged = current_room.hanged)
			elif current_room.is_day == True:
				players = User.all().filter("room =", current_room_name)
				current_role = self.request.cookies.get('role')
				self.render("day.html", players = players, current_role = current_role, murdered = current_room.murdered)				

		else:
			self.redirect('/newuser')

	def post(self):
		current_room_name = self.request.cookies.get('room')
		current_room = Room.all().filter("name =", current_room_name).get()
		players = User.all().filter("room =", current_room_name).fetch(limit=None)
		total_players = len(players)
		if total_players > 1:
			mafia_list = sample(players, (total_players+1)/3)
			for each_mafia in mafia_list:
				each_mafia.role = 1
			db.put(mafia_list)

			current_room.in_progress = True
			current_room.put()
			self.redirect('/game')
		else:
			self.redirect('/newuser')

class Proceed(Handler):
	def post(self):
		current_room_name = self.request.cookies.get('room')
		current_room = Room.all().filter("name =", current_room_name).get()
		if current_room.is_day == None:
			current_room.is_day = False
		else:
			current_room.is_day = not current_room.is_day
		current_room.put()
		self.redirect('/game')		

class NightVotes(Handler):
	def post(self):
		current_user = User.all().filter("name =", self.request.cookies.get('user')).get()		
		if current_user.role == 1:
			current_user.vote = self.request.get('vote')
			current_user.put()
		if self.request.cookies.get('room_admin') == 'True':
			mafia = User.all().filter("room =", self.request.cookies.get('room')).filter("role =", 1).filter("is_alive =", True)
			first_vote = mafia[0].vote
			for each_mafia in mafia:
				if each_mafia.vote != first_vote:
					first_vote = ""
				each_mafia.vote = ""
				each_mafia.put()
			current_room_name = self.request.cookies.get('room')
			current_room = Room.all().filter("name =", current_room_name).get()		
			if first_vote:
				murdered_user = User.all().filter("room =", self.request.cookies.get('room')).filter("name =", first_vote).get()
				murdered_user.is_alive = False
				current_room.murdered = murdered_user.name
				murdered_user.put()				
				current_room.hanged = ""
			current_room.is_day = not current_room.is_day
			current_room.put()
		self.redirect('/game')		

class DayVotes(Handler):
	def post(self):
		current_user = User.all().filter("name =", self.request.cookies.get('user')).get()		
		current_user.vote = self.request.get('vote')
		current_user.put()
		if self.request.cookies.get('room_admin') == 'True':
			all_players = User.all().filter("room =", self.request.cookies.get('room')).filter("is_alive =", True)
			count_votes = dict()
			for each in all_players:
				if each.vote != "":
					count_votes[each.vote] = count_votes.get(each.vote, 0) + 1
				each.vote = ""
				each.put()
				current_room_name = self.request.cookies.get('room')
				current_room = Room.all().filter("name =", current_room_name).get()
				current_room.murdered = ""
				current_room.hanged = max(count_votes.items(), key=lambda x: x[1])[0]
				hanged_user = User.all().filter("room =", current_room_name).filter("name =", current_room.hanged).get()
				hanged_user.is_alive = False
				hanged_user.put()
				current_room.is_day = not current_room.is_day
				current_room.put()
		self.redirect('/game')


class Room(db.Model):
	name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	admin = db.StringProperty(required = True)
	in_progress = db.BooleanProperty(required = True)
	is_day = db.BooleanProperty()
	murdered = db.StringProperty()
	hanged = db.StringProperty()	

class User(db.Model):
	name = db.StringProperty(required = True)
	room = db.StringProperty(required = True)
	email = db.StringProperty(required = True)
	role = db.IntegerProperty()
	is_alive = db.BooleanProperty()
	vote = db.StringProperty()

