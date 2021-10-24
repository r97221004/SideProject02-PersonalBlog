from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor # 要有 flask-wtf 的套件

bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()