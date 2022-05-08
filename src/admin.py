from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['POST', 'GET'])
@login_required
def admin_panel():
    if current_user.is_authenticated:
        user = User.query.get(int(current_user.get_id()))
        if not user.admin:
            return redirect(url_for('index'))
    users = User.query.order_by(User.id).all()
    if request.method == 'POST':
        if 'edit_user' in request.form:
            old_username = request.form['edit_user']
            user = User.query.filter_by(username=old_username).first()
            username = request.form['username']
            password = request.form['password']
            if len(username) > 0:
                user.username = username
            if len(password) > 0:
                if len(password) >= 3:
                    user.password = generate_password_hash(password, method='sha256')
                else:
                    flash('Password must be minimum 3 characters long')
            if 'grant_admin' in request.form:
                user.admin = True
            if 'remove_admin' in request.form:
                user.admin = False
        if 'delete' in request.form:
            old_username = request.form['delete']
            User.query.filter_by(username=old_username).delete()
        db.session.commit()
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin_panel.html', users=users)



