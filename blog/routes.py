#!/usr/bin/env python3
from flask import request,redirect,render_template,url_for,session,flash,escape
from .libs.mysql import SQL
from .libs.time import date
from .libs.config import *
from blog import app,sql,csrf
from PIL import Image
from flask_login import login_user, current_user, logout_user,login_required
from .forms import RegistrationForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os,secrets

def allowed_file(filename,allow):
	return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in allow
@app.route('/')
def index():
	return render_template('home.html')
@app.route('/@<user>')
def show_user(user):
	c , cmd = sql.mysql()
	cmd.execute('SELECT image,username,about,email FROM users WHERE username = (%s)',(user,))
	data = cmd.fetchall()
	data = [dict(profile_pic=row[0], name=escape(row[1]),about=escape(row[2]),email=escape(row[3])) for row in data]
	return render_template('profile.html',user_data=data)
@app.route('/profile')
def show_profile():
	if session.get('username'):
		pass
	else:
		flash('Login First')
		return redirect(url_for('login'))
	c , cmd = sql.mysql()
	cmd.execute('SELECT image,username,about,email FROM users WHERE username = (%s)',(session.get('username'),))
	data = cmd.fetchall()
	data = [dict(profile_pic=row[0], name=row[1],about=row[2],email=row[3]) for row in data]
	return render_template('profile.html',user_data=data)
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		c , cmd = sql.mysql()
		r = request.form
		cmd.execute('SELECT user_id,username FROM users WHERE username = (%s)',(r['username'],))
		data = cmd.fetchone()
		if data:
			cmd.execute('SELECT password FROM users WHERE username = (%s)',(r['username'],))
			the_pass = cmd.fetchone()
			if the_pass:
				data = check_password_hash(the_pass[0],r['password'])
				if data:
					session['username'] = r['username']
					return redirect(url_for('show_profile'))
		flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)
@app.route('/upload',methods=['POST','GET'])
def upload_image():
	if request.method == 'POST':
		if session.get('username'):
			pass
		else:
			return redirect(url_for('login'))
		file = request.files['file']
		filename = secure_filename(file.filename)
		filename = secrets.token_hex(8) + '_' + filename
		if allowed_file(filename,allow={'jpg','png','jpeg','gif'}):
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			i = Image.open(f'blog/static/image/{filename}')
			i.thumbnail((125,125))
			i.save(f'blog/static/image/{filename}')
			c , cmd = sql.mysql()
			cmd.execute('UPDATE users SET image = (%s) WHERE username = (%s)',(filename,session.get('username'),))
			c.commit()
		else:
			flash('Not Allowed')
		return redirect(url_for('show_profile'))
	else:
		return render_template('upload_image.html')
@app.route('/register',methods=['POST','GET'])
def register_page():
	form = RegistrationForm()
	if form.validate_on_submit():
		c,cmd = sql.mysql()
		r = request.form
		if '@' not in r['email']:
			flash('Add a Validate email .!')
			return redirect(url_for('register'))
		password = generate_password_hash(r['password'])
		cmd.execute("INSERT INTO users(`username`,`password`,`about`,`date`,`image`,`email`) VALUES (%s,%s,%s,%s,%s,%s);",(r['username'],password,'Normal User',date(),'normal.jpg',r['email']))
		c.commit()
		flash('Login Unsuccessful. Please check email and password')
	return render_template('register.html', title='Register', form=form)
if __name__ == '__main__':
	manager.run()
