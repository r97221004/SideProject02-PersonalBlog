from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, SelectField, StringField
from wtforms.fields.simple import HiddenField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import URL, DataRequired, Email, Length, ValidationError, Optional

from PersonalBlog.models import Category


class LoginForm(FlaskForm):
    username = StringField(label = '使用者帳號', validators = [DataRequired(), Length(1, 20)])
    password = PasswordField(label = '使用者密碼', validators =[DataRequired(), Length(1, 128)])
    remember = BooleanField(label = '記得我')
    submit = SubmitField(label = '登入')


class SettingForm(FlaskForm):
    name = StringField(label = '姓名', validators = [DataRequired(), Length(1, 70)])
    blog_title = StringField(label = '部落格標題', validators = [DataRequired(), Length(1, 60)])
    bolg_sub_title = StringField(label = '部落格副標題', validators = [DataRequired(), Length(1, 100)])
    about = CKEditorField(label = '關於我', validators = [DataRequired()])
    submit = SubmitField(label = '更改送出')


class PostForm(FlaskForm):
    title = StringField(label = '標題', validators = [DataRequired(), Length(1, 60)])
    category = SelectField(label = '文章分類', coerce = int, default = 1) # 選擇值默認為字符串類型，我們使用 coerce 關鍵字指定數據類型為整型
    body = CKEditorField(label = '內文', validators = [DataRequired()])
    submit = SubmitField(label = '送出')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all() ]
        # choices 必須是一個包含兩元素元組的列表，列表中的元組分別包含選項值和選項標籤。我們使用分類的id作為選項值，分類的名稱作為選項標籤


class CategoryForm(FlaskForm):
    name = StringField(label = '分類名稱', validators = [DataRequired(), Length(1, 30)])
    submit = SubmitField(label = '送出')

    def validate_name(self, field):
        if Category.query.filter_by(name = field.data).first():
            raise ValidationError('分類名稱已經使用中')


class CommentForm(FlaskForm):
    author = StringField(label = '名字', validators = [DataRequired(), Length(1, 30)])
    email = StringField(label = '電子信箱', validators = [DataRequired(), Email(), Length(1, 254)]) # 需要 pip install email-validator
    site = StringField(label = '個人網站', validators = [Optional(), URL(), Length(0, 255)])
    body = TextAreaField(label = '評論', validators = [DataRequired()])
    submit = SubmitField(label = '送出')
        

class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField(label = '社群網站名稱', validators = [DataRequired(), Length(1, 30)])
    url = StringField(label = '網址', validators = [DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField(label = '送出')

