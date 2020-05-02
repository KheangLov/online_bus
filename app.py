from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from data import About
import requests
import os

csrf = CSRFProtect()
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
csrf.init_app(app)
app.debug = True

Province = About()

@app.route('/')
def index():
    token = session.get('token', '')
    if token == '':
        return redirect(url_for('login'))
    user = session.get('user', '')
    if user != '':
        user = eval(user)
    return render_template('index.html', token=token, user=user)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/bus')
def bus():
    return render_template('bus.html')

@app.route('/taxi')
def taxi():
    return render_template('taxi.html')

@app.route('/ferri')
def ferri():
    return render_template('ferri.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/book-now')
def bookNow():
    return render_template('book-now.html')

@app.route('/login')
def login():
    error = request.args.get('error', '')
    if error != '':
        return render_template('auth/login.html', error=error)
    success = request.args.get('success', '')
    if success != '':
        return render_template('auth/login.html', success=success)
    token = session.get('token', '')
    if token != '':
        return redirect(url_for('index'))
    return render_template('auth/login.html')

@app.route('/handle_login', methods=['POST'])
def handle_login():
    email = request.form['email'].strip()
    password = request.form['password'].strip()
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post('http://127.0.0.1:5000/api/auth/login', json=payload)
    data = response.json()
    if 'error' in data:
        return redirect(url_for('login', error=data['error']))
    session['token'] = data['token']
    session['user'] = data['user']
    return redirect(url_for('index'))

@app.route('/register')
def register():
    error = request.args.get('error', '')
    if error != '':
        return render_template('auth/register.html', error=error)
    token = session.get('token', '')
    if token != '':
        return redirect(url_for('index'))
    return render_template('auth/register.html')

@app.route('/handle_register', methods=['POST'])
def handle_register():
    name = request.form['name'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()
    confirm = request.form['password_confirm'].strip()

    if password != confirm:
        return redirect(url_for('register', error='Password not match!'))

    payload = {
        'name': name,
        'email': email,
        'password': password
    }
    response = requests.post('http://127.0.0.1:5000/api/auth/register', json=payload)
    data = response.json()
    if 'error' in data:
        return redirect(url_for('register', error=data['error']))
    success = 'User have been registered!'
    return redirect(url_for('login', success=success))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/forgot')
def forgot():
    success = request.args.get('success', '')
    if success != '':
        return render_template('auth/forgot_password.html', success=success)
    error = request.args.get('error', '')
    if error != '':
        return render_template('auth/forgot_password.html', error=error)
    return render_template('auth/forgot_password.html', success=success)

@app.route('/handle_forgot', methods=['POST'])
def handle_forgot():
    email = request.form['email'].strip()
    payload = {
        'email': email
    }
    response = requests.post('http://127.0.0.1:5000/api/auth/forgot', json=payload)
    data = response.json()
    if 'error' in data:
        return redirect(url_for('forgot', error=data['error']))
    success = 'Reset token sent!'
    return redirect(url_for('forgot', success=success))

@app.route('/reset')
def reset():
    reset_token = request.args.get('reset_token', '')
    success = request.args.get('success', '')
    if success != '':
        return render_template('auth/reset_password.html', success=success)
    error = request.args.get('error', '')
    if error != '':
        return render_template('auth/reset_password.html', error=error)
    return render_template('auth/reset_password.html', success=success, reset_token=reset_token)

@app.route('/handle_reset', methods=['POST'])
def handle_reset():
    reset_token = request.form['reset_token'].strip()
    if reset_token == '':
        return redirect(url_for('reset', error='Reset token required!'))

    password = request.form['password'].strip()
    payload = {
        'password': password,
        'reset_token': reset_token
    }
    response = requests.post('http://127.0.0.1:5000/api/auth/reset', json=payload)
    data = response.json()
    if 'error' in data:
        return redirect(url_for('reset', error=data['error']))
    success = 'Password updated!'
    return redirect(url_for('reset', success=success))


if __name__ == '__main__':
    app.run()
