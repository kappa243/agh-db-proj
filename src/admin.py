from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['POST', 'GET'])
@login_required
def admin_panel():
    users = User.query.order_by(User.id).all()
    if request.method == 'POST':
        if 'edit_user' in request.form:
            old_username = request.form['edit_user']
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=old_username).first()
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
            db.session.commit()
    return render_template('admin_panel.html', users=users)



