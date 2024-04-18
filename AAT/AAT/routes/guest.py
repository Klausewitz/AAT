from flask import flash, redirect, render_template, url_for
from flask_login import logout_user, current_user
from forms.users_form import LoginForm
from models.models import UserService
from routes import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        result = UserService().login_action(username, password=form.password.data)
        if result:
            flash(f'Welcome {username}', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or / and password', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(401)
def ERROR_401(e):
    return render_template('error/401.html')


@app.errorhandler(404)
def ERROR_404(e):
    return render_template('error/404.html')