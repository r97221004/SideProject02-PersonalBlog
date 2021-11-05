from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor # 要有 flask-wtf 的套件
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from PersonalBlog.models import Admin
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
login_manager.login_message = '為了拜訪這個網頁, 請先登入｡'
login_manager.login_message_category = 'warning' # 選擇 flash 閃現所使用的類別
