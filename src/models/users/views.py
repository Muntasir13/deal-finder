from flask import Blueprint, request, session, render_template, url_for
from werkzeug.utils import redirect

from models.users.users import Users
import models.users.errors as UserErrors


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('reg_user', None)
        owner = request.form.get('reg_owner', None)

        if user:
            return redirect(url_for('register_user', user_type='user'))
        elif owner:
            return redirect(url_for("register_user", user_type='owner'))

    return render_template("registration.html")


@users_blueprint.route('/<string:user_type>/register', methods=['GET', 'POST'])
def register_user(user_type):
    if request.method == 'POST':
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password_1', None)
        confirm_pass = request.form.get('password_2', None)
        institution = request.form.get('institution_name', None) if user_type is 'owner' else None
        try:
            if Users.register_user(str(username), str(email), str(password), str(confirm_pass), str(user_type), str(institution)):
                return redirect(url_for('users.login'))
        except UserErrors.UserErrors as e:
            return e.message

    if user_type == 'user':
        return render_template("reg_user.html")
    elif user_type == 'owner':
        return render_template("reg_owner.html")


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = str(request.form.get('username', None))
        password = str(request.form.get('password', None))

        try:
            if Users.login_is_valid(username, password):
                session['username'] = username
                session['logged_in'] = True
                return redirect(url_for("index"))
        except UserErrors.UserErrors as e:
            return e.message

    return render_template("login.html")


@users_blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("index"))


@users_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_pass():
    if request.method == 'POST':
        username = request.form.get('username', None)
        email = request.form.get('email', None)

        try:
            if Users.get_by_email(username, email):
                session['username'] = username
                return redirect(url_for('users.recover_pass', username=username))
        except UserErrors.UserErrors as e:
            return e.message

    return render_template("pass.html")


@users_blueprint.route('/<string:username>/recover_password', methods=['GET', 'POST'])
def recover_pass(username):
    if request.method == 'POST':
        password_1 = request.form.get('password_1', None)
        password_2 = request.form.get('password_2', None)

        try:
            if Users.update_password(username, password_1, password_2):
                return redirect(url_for("users.login"))
        except UserErrors.UserErrors as e:
            return e.message

    return render_template("recover_pass.html")
