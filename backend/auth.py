import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv
from database import get_users_collection

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token(user_id, email):
    """Generate JWT token for user"""
    payload = {
        'user_id': str(user_id),
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token):
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Get user from database
        users_collection = get_users_collection()
        user = users_collection.find_one({'email': payload['email']})
        
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        # Pass user to route
        return f(current_user=user, *args, **kwargs)
    
    return decorated

def create_user(email, password=None, name=None, google_id=None, picture=None):
    """Create a new user in database"""
    users_collection = get_users_collection()
    
    user_data = {
        'email': email,
        'name': name or email.split('@')[0],
        'created_at': datetime.utcnow(),
        'last_login': datetime.utcnow(),
        'picture': picture,
        'auth_provider': 'google' if google_id else 'email'
    }
    
    if password:
        user_data['password'] = hash_password(password)
    
    if google_id:
        user_data['google_id'] = google_id
    
    try:
        result = users_collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data
    except Exception as e:
        return None

def get_user_by_email(email):
    """Get user by email"""
    users_collection = get_users_collection()
    return users_collection.find_one({'email': email})

def get_user_by_google_id(google_id):
    """Get user by Google ID"""
    users_collection = get_users_collection()
    return users_collection.find_one({'google_id': google_id})

def update_last_login(email):
    """Update user's last login time"""
    users_collection = get_users_collection()
    users_collection.update_one(
        {'email': email},
        {'$set': {'last_login': datetime.utcnow()}}
    )
