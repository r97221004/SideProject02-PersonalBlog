from threading import Thread
from flask import current_app, url_for
from flask_mail import Message
from PersonalBlog.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    app = current_app._get_current_object() # 獲取被代理的真實對象
    message = Message(subject, recipients = [to], html = html)
    thr = Thread(target = _send_async_mail, args = [app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id = post.id, _external = True) + '#comments'
    send_mail(subject = '新的評論', to = current_app.config['BLUELOG_EMAIL'],
    html = f'<p>在文章【<i>{post.title}</i>】有新的評論, 請點選以下連結查看｡</p>'
           f'<p><a href="{post_url}">{post_url}</a></p>'
           f'<p><small style="color: #868e96">不要直接回覆此訊息｡</small></p>'
    )


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_mail(subject='New reply', to=comment.email,
              html='<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (comment.post.title, post_url, post_url))