import random
from faker import Faker

from PersonalBlog.extensions import db
from PersonalBlog.models import Admin, Category, Post, Comment, Link

fake = Faker('zh_TW')


def fake_admin():
    admin = Admin(
        username = 'Matt',
        blog_title = '用程式寫生活',
        blog_sub_title = '紀錄是為了走更長遠的路, 與您互動是我最大的動力｡',
        name = 'Matt',
        about = '我是張家豪,有接近十年的教學經驗｡ 近年開始自學與進修, 人生的下半場以資料分析師跟後端工程師為目標, 您的寶貴經驗與意見會是我最大的動力, 歡迎留言給我｡'
    )
    db.session.add(admin)
    db.session.commit()


def fake_categories(count = 10):
    category = Category(name = '綜合')
    db.session.add(category)

    categories = ['程式討論', '工作雜記', '美食', '健身', '敗家', '保健', '愛情', '朋友', '投資', '八卦']
    for i in range(count):
        if i <= 9:
            category = Category(name = categories[i])
            db.session.add(category)
            db.session.commit()
        else:
            category = Category(name = fake.word())
            db.session.add(category)
            try:
                db.session.commit()
            except:
                db.session.rollback()


def fake_posts(count = 50):
    for i in range(count):
        post = Post(
            title = fake.sentence(),
            body = fake.text(2000),
            category = Category.query.get(random.randint(1, Category.query.count())),
            timestamp = fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count = 500):
    for i in range(count):
        comment = Comment(
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True,
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    
    salt = int(count*0.1)
    for i in range(salt):
        # unreviewed comments
        comment = Comment(
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = False,
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author = 'Matt',
            email='r97221004@gmail.com',
            site='http://r97221004.pythonanywhere.com/',
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            from_admin = True,
            reviewed = True,
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for i in range(salt):
        comment = Comment(
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True,
            replied = Comment.query.get(random.randint(1, Comment.query.count())),
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    facebook = Link(name = 'Facebook', url = 'https://www.facebook.com/profile.php?id=100001430323403')
    linkedin = Link(name='LinkedIn', url='https://www.linkedin.com/in/%E5%AE%B6%E8%B1%AA-%E5%BC%B5-3b92b7163/')
    cakeresume = Link(name = 'CakeResume', url ='https://www.cakeresume.com/me/r97221004')
    github = Link(name = 'Github', url = 'https://github.com/r97221004')
    db.session.add_all([facebook, linkedin, cakeresume, github])
    db.session.commit()
