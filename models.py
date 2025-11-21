from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))  # Radiobutton: Male/Female/Other
    birth_place = db.Column(db.String(100))  # Combobox
    school = db.Column(db.String(100))  # Combobox
    hobbies = db.Column(db.String(500))  # Checkbox values stored as comma-separated
    about = db.Column(db.Text)  # Textarea
    profile_photo = db.Column(db.String(255))
    
    # Activity tracking
    current_location = db.Column(db.String(100))
    current_activity = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    photos = db.relationship('Photo', backref='user', lazy=True, cascade='all, delete-orphan')
    videos = db.relationship('Video', backref='user', lazy=True, cascade='all, delete-orphan')
    forum_posts = db.relationship('ForumPost', backref='author', lazy=True, cascade='all, delete-orphan')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy=True)
    location = db.relationship('Location', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Photo(db.Model):
    """Photo model for image uploads"""
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255))
    caption = db.Column(db.String(500))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tags = db.relationship('PhotoTag', backref='photo', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Photo {self.filename}>'


class PhotoTag(db.Model):
    """Photo tag model for image map tagging"""
    __tablename__ = 'photo_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False)
    tagged_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # HTML image map attributes
    shape = db.Column(db.String(20), nullable=False)  # rect, circle, poly
    coords = db.Column(db.String(200), nullable=False)  # Coordinates as string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    tagged_user = db.relationship('User', foreign_keys=[tagged_user_id])
    
    def __repr__(self):
        return f'<PhotoTag {self.shape} on Photo {self.photo_id}>'


class Video(db.Model):
    """Video model for YouTube embeds"""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    youtube_url = db.Column(db.String(255), nullable=False)
    youtube_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Video {self.title}>'


class ForumPost(db.Model):
    """Forum post model for public discussions"""
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('ForumReply', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ForumPost {self.title}>'


class ForumReply(db.Model):
    """Forum reply model for post responses"""
    __tablename__ = 'forum_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    author = db.relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<ForumReply on Post {self.post_id}>'


class Message(db.Model):
    """Private message model for user-to-user messaging"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.recipient_id}>'


class Location(db.Model):
    """Location model for map feature"""
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Location for User {self.user_id}>'
