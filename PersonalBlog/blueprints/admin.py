from operator import pos
from flask import Blueprint, render_template, url_for, redirect, request, current_app, flash
from flask_login import login_required

from PersonalBlog.extensions import db
from PersonalBlog.forms import CategoryForm, LinkForm, PostForm, SettingForm
from PersonalBlog.models import Category, Post, Comment
from PersonalBlog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    return render_template('admin/settings.html', form = form)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type = int )
    per_page = current_app.config['BLUELOG_MANAGE_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page = page, per_page = per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', page = page, pagination = pagination, posts = posts)


@admin_bp.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title = title, body = body, category = category)
        db.session.add(post)
        db.session.commit()
        flash('新增文章成功', 'success')
        return redirect(url_for('blog.show_post', post_id = post.id))
    return render_template('admin/new_post.html', form = form)


@admin_bp.route('/post/<int:post_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('文章編輯成功', 'success')
        return redirect(url_for('blog.show_post', post_id = post.id))

    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id

    return render_template('admin/edit_post.html', form = form)


@admin_bp.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已經刪除', 'success')
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/set-comment', methods = ['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('禁止評論', 'success')
    else:
        post.can_comment = True
        flash('允許評論', 'success')

    db.session.commit()
    return redirect_back()


@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all') # 'all', 'unreviewed', 'admin'
    page = request.args.get('page', 1, type = int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed = False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin  = True)
    else:
        filtered_comments = Comment.query

    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page = page, per_page = per_page)
    comments = pagination.items
    return render_template('admin/manager_comment.html', comments = comments, pagination = pagination)


@admin_bp.route('/comment/<int:comment_id>/approve', methods = ['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('評論已經公開', 'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods = ['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('評論已刪除', 'success')
    return redirect_back()


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html') # categories 已在模板上下文


@admin_bp.route('category/new', methods = ['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name = name)
        db.session.add(category)
        db.session.commit()
        flash('新增分類成功', 'success')
        return redirect(url_for('admin.manage_category'))
    return render_template('admin/new_category.html', form = form)


@admin_bp.route('/category/<int:category_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('無法編輯綜合分類', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('分類名稱更新成功', 'success')
        return redirect(url_for('admin.manage_category'))

    form.name.data = category.name
    return render_template('admin/edit_category.html', form = form)


@admin_bp.route('/category/<int:category_id>/delete', methods = ['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('綜合分類無法刪除', 'warning')
        return redirect(url_for('blog.index'))
    category.delete() # 自定義方法
    flash('分類已刪除', 'success')
    return redirect(url_for('admin.manage_category'))


@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html') # links 已在模板上下文


@admin_bp.route('/link/new', methods = ['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    return render_template('admin/new_link.html', form = form)


@admin_bp.route('/link/<int:link_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    return render_template('admin/edit_link.html', form = form)


@admin_bp.route('/link/<int:link_id>/delete', methods = ['POST'])
@login_required
def delete_link(link_id):
    return redirect(url_for('admin.manage_link'))

