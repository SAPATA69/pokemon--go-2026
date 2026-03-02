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
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # แก้ไข: ใช้ sa.select
        query = sa.select(User).where(User.username==username)
        user = db.session.scalar(query)
        
        if user:
            flash('ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว!', 'warning')
            return redirect(url_for('users.register'))
        else:
            query = sa.select(User).where(User.email==email)
            user = db.session.scalar(query)
            
            if user:
                flash('อีเมลนี้มีอยู่ในระบบแล้ว!', 'warning')
                return redirect(url_for('users.register'))
            else:
                if password == confirm_password:
                    pwd_hash = bcrypt.generate_password_hash(password=password).decode('utf-8')
                    user = User(username=username, email=email, password=pwd_hash)
                    db.session.add(user)
                    db.session.commit()
                    flash('ลงทะเบียนสำเร็จ!', 'success')
                    return redirect(url_for('users.login'))
                else:
                    flash('รหัสผ่านไม่ตรงกัน!', 'warning')
                    return redirect(url_for('users.register'))
                    
    return render_template('users/register.html', title='Register Page')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # แก้ไข: ใช้ sa.select
        query = sa.select(User).where(User.username==username)
        user = db.session.scalar(query)
        
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash('เข้าสู่ระบบสำเร็จ!', 'success')
                return redirect(url_for('users.index'))
            else:
                flash('รหัสผ่านไม่ถูกต้อง!', 'warning')
                return redirect(url_for('users.login'))
        else:
            flash('ไม่พบชื่อผู้ใช้นี้!', 'warning')
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
        lastname = request.form.get('lastname')
        
        if len(firstname) > 0 and len(lastname) > 0:
            user.firstname = firstname
            user.lastname = lastname
            db.session.add(user)
            db.session.commit()
            flash('อัพเดทโปรไฟล์สำเร็จ!', 'success')
            return redirect(url_for('users.profile'))
    
    return render_template('users/profile.html', 
                         title='Profile Page',
                         user=user)