from flask import Blueprint, render_template, current_app, request, url_for, flash
from werkzeug.utils import redirect

from PersonalBlog.emails import send_new_comment_email, send_new_reply_email
from PersonalBlog.extensions import db
from PersonalBlog.models import Admin, Category, Post, Comment
from PersonalBlog.forms import AdminCommentForm, CommentForm
from flask_login import current_user

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type = int) # 從查詢字符串獲取當前頁數
    per_page = current_app.config['BLUELOG_POST_PER_PAGE'] # 每頁數量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page = per_page)
    posts = pagination.items # 當前頁數的記錄列表
    return render_template('blog/index.html', pagination = pagination, posts = posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type = int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # 如果我們直接調用 category.posts，會以列表的形式返回該分類下的所有文章對象，但是我們需要對這些文章記錄附加其他查詢過濾器和方法， 所以不能用這個方法。
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page) 
    posts = pagination.items
    return render_template('blog/category.html', category = category, pagination = pagination, posts = posts)


@blog_bp.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type = int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed = True).order_by(Comment.timestamp.asc()).paginate(page, per_page) # 只有審核過的才會顯示
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = current_app.config['BLUELOG_SITE']
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False
    
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author = author, email = email, site = site, body = body, 
                          from_admin = from_admin, reviewed = reviewed, post = post)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)            
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('評論已送出', 'success')
        else:
            flash('非常感謝, 你的評論會在審查成功後送出｡', 'info')
            send_new_comment_email(post)
        return redirect(url_for('blog.show_post', post_id = post_id))
    return render_template('blog/post.html', post = post, pagination = pagination, form = form, comments = comments)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('blog.show_post', post_id = comment.post_id, reply = comment_id, author = comment.author) + '#comment-form')