# app/oauth.py
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, url_for, session, jsonify
import os
from .models import db, User

oauth = OAuth()
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='github',
        client_id=os.getenv('GITHUB_CLIENT_ID'),
        client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )

@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@auth_bp.route('/callback')
def callback():
    token = oauth.github.authorize_access_token()
    user_data = oauth.github.get('user').json()
    email = user_data.get('email')

    if not email:
        emails = oauth.github.get('user/emails').json()
        primary = next((e['email'] for e in emails if e.get('primary')), None)
        email = primary or emails[0]['email']

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.id
    return jsonify({
        "token": user.id,
        "email": user.email
    })

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')
