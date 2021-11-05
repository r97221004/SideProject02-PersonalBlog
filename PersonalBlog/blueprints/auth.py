from flask import Blueprint, render_template, url_for, redirect, flash

from flask_login import current_user, login_user, logout_user
from PersonalBlog.forms import LoginForm
from PersonalBlog.models import Admin
from PersonalBlog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            # 驗證用戶名和密碼
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember) # 登入用户
                flash('歡迎回來', 'info')
                return redirect_back() # 返回上一个頁面
            flash('使用者帳號或密碼輸入錯誤', 'warning')
        else:
            flash('沒有設定任何管理者', 'warning')           
    return render_template('auth/login.html', form = form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('登出成功', 'info')
    return redirect_back()