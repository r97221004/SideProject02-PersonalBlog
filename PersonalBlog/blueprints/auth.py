from flask import Blueprint, render_template

from PersonalBlog.forms import LoginForm
from PersonalBlog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form = form)


@auth_bp.route('/logout')
def logout():
    return redirect_back()