from flask import Blueprint, render_template, current_app, request

from PersonalBlog.models import Post

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
    return render_template('blog/category.html')


@blog_bp.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post = post)