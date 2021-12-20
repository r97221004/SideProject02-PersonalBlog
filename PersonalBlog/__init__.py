import os
import click
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from PersonalBlog.blueprints.blog import blog_bp
from PersonalBlog.blueprints.admin import admin_bp
from PersonalBlog.blueprints.auth import auth_bp
from PersonalBlog.extensions import bootstrap, db, ckeditor, mail, moment, login_manager, csrf
from PersonalBlog.models import Admin, Category, Comment, Link, Post
from PersonalBlog.settings import config


# 工廠函數接收配置名稱作為參數，這允許我們在程序的不同位置傳入不同的配置來創建程序實例。
def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('PersonalBlog') 
    app.config.from_object(config[config_name])

    register_logging(app) # 註冊日誌，現在不會用到!
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)
    register_commands(app)

    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix = '/admin')
    app.register_blueprint(auth_bp, url_prefix = '/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db = db, Admin = Admin, Post = Post, Category = Category)  # 建表要把表放置在 shell 上下文處理函數


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed = False).count()
        else:
            unread_comments = None

        return dict(admin = admin, categories = categories, links = links, unread_comments = unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_carf_error(e):
        return render_template('errors/400.html', description = e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag = True, help = 'Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort = True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
    

    @app.cli.command()
    @click.option('--category', default = 10,  help = 'Quantity of categories, default is 10.')
    @click.option('--post', default = 50, help = 'Quantity of posts, default is 50.')
    @click.option('--comment', default = 500, help = 'Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""

        from PersonalBlog.fakes import fake_admin, fake_categories, fake_comments, fake_links, fake_posts

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo(f'Generating {category} categories...')
        fake_categories(category)

        click.echo(f'Generating {post} posts...')
        fake_posts(post)

        click.echo(f'Generating {comment} comments...')
        fake_comments(comment)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')


    @app.cli.command()
    @click.option('--username', prompt = True, help = 'The username used to login.')
    @click.option('--password', prompt = True, hide_input = True, confirmation_prompt = True, help = 'The password used to login.')
    def admin(username, password):
        """Building Blog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None: # 如果數據庫中已經有管理員記錄就更新用戶名和密碼
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)

        else: # 否則創建新的管理員記錄
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username = username,
                blog_title = '用程式寫生活',
                blog_sub_title = "紀錄是為了走更長遠的路, 與您互動是我最大的動力｡",
                name = 'Matt',
                about = '我是張家豪,有接近十年的教學經驗｡ 近年開始自學與進修, 人生的下半場以資料分析師跟後端工程師為目標, 您的寶貴經驗與意見會是我最大的動力, 歡迎留言給我｡'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name = '綜合')
            db.session.add(category)
        
        db.session.commit()
        click.echo('Done.')