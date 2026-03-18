from flask import Blueprint, render_template, request, redirect, url_for, flash
from pokemon.extensions import db, bcrypt
from pokemon.models import User
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/')
@login_required
def index():
    return render_template('users/index.html', title='User Page')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email    = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        query = sa.select(User).where(User.username == username)
        user = db.session.scalar(query)
        if user:
            flash('ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว!', 'warning')
            return redirect(url_for('users.register'))

        query = sa.select(User).where(User.email == email)
        user = db.session.scalar(query)
        if user:
            flash('อีเมลนี้มีอยู่ในระบบแล้ว!', 'warning')
            return redirect(url_for('users.register'))

        if password != confirm_password:
            flash('รหัสผ่านไม่ตรงกัน!', 'warning')
            return redirect(url_for('users.register'))

        pwd_hash = bcrypt.generate_password_hash(password=password).decode('utf-8')
        user = User(username=username, email=email, password=pwd_hash)
        db.session.add(user)
        db.session.commit()
        flash('ลงทะเบียนสำเร็จ!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register Page')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query = sa.select(User).where(User.username == username)
        user = db.session.scalar(query)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('เข้าสู่ระบบสำเร็จ!', 'success')
            return redirect(url_for('users.index'))
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!', 'warning')
            return redirect(url_for('users.login'))

    return render_template('users/login.html', title='Login Page')


@users_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname  = request.form.get('lastname')
        if len(firstname) > 0 and len(lastname) > 0:
            user.firstname = firstname
            user.lastname  = lastname
            db.session.add(user)
            db.session.commit()
            flash('อัพเดทโปรไฟล์สำเร็จ!', 'success')
            return redirect(url_for('users.profile'))

    return render_template('users/profile.html', title='Profile Page', user=user)


# ── เปลี่ยนรหัสผ่าน ──────────────────────────────────────────────
@users_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password     = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # ตรวจสอบรหัสผ่านปัจจุบัน
        if not bcrypt.check_password_hash(current_user.password, current_password):
            flash('รหัสผ่านปัจจุบันไม่ถูกต้อง!', 'danger')
            return redirect(url_for('users.change_password'))

        # ตรวจสอบรหัสผ่านใหม่ตรงกัน
        if new_password != confirm_password:
            flash('รหัสผ่านใหม่ไม่ตรงกัน!', 'warning')
            return redirect(url_for('users.change_password'))

        # ตรวจสอบความยาวรหัสผ่านใหม่
        if len(new_password) < 6:
            flash('รหัสผ่านใหม่ต้องมีอย่างน้อย 6 ตัวอักษร!', 'warning')
            return redirect(url_for('users.change_password'))

        # บันทึกรหัสผ่านใหม่
        current_user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        flash('เปลี่ยนรหัสผ่านสำเร็จ!', 'success')
        return redirect(url_for('users.profile'))

    return render_template('users/change_password.html', title='Change Password')