from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required

from PersonalBlog.forms import CategoryForm, LinkForm, PostForm, SettingForm
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
    return render_template('admin/manage_post.html')


@admin_bp.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    return render_template('admin/new_post.html', form = form)


@admin_bp.route('/post/<int:post_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_post():
    form = PostForm()
    return render_template('admin/edit_post.html', form = form)


@admin_bp.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post():
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/set-comment', methods = ['POST'])
@login_required
def set_comment(post_id):
    return redirect_back()


@admin_bp.route('/comment/manage')
@login_required
def manager_comment():
    return render_template('admin/manager_comment.html')


@admin_bp.route('/comment/<int:comment_id>/approve', methods = ['POST'])
@login_required
def approve_comment(comment_id):
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods = ['POST'])
@login_required
def delete_comment(comment_id):
    return redirect_back()


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('category/new', methods = ['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    return render_template('admin/new_category.html', form = form)


@admin_bp.route('/category/<int:category_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_category():
    form = CategoryForm()
    return render_template('admin/edit_category.html', form = form)


@admin_bp.route('/category/<int:category_id>', methods = ['POST'])
@login_required
def delete_category(category_id):
    return redirect(url_for('admin.manage_category'))


@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')


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

