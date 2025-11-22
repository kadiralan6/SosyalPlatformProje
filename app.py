import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, User, Photo, PhotoTag, Video, ForumPost, ForumReply, Message, Location
from forms import (RegistrationForm, LoginForm, ProfileForm, PhotoUploadForm, 
                   VideoForm, ForumPostForm, ForumReplyForm, MessageForm, LocationForm)
from utils import save_uploaded_file, create_thumbnail, extract_youtube_id, get_youtube_embed_url

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails'), exist_ok=True)

# Create database tables on startup (for production deployment)
with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def index():
    """Homepage"""
    recent_posts = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(5).all()
    return render_template('index.html', recent_posts=recent_posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            birth_place=form.birth_place.data,
            school=form.school.data,
            hobbies=form.hobbies.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        
        # Handle profile photo
        if form.profile_photo.data:
            filename = save_uploaded_file(form.profile_photo.data, app.config['UPLOAD_FOLDER'])
            if filename:
                user.profile_photo = filename
                # Create thumbnail
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', filename)
                create_thumbnail(image_path, thumbnail_path)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Hoş geldiniz, {user.first_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('index'))

@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    """View user profile"""
    user = User.query.get_or_404(user_id)
    photos = Photo.query.filter_by(user_id=user_id).order_by(Photo.uploaded_at.desc()).all()
    videos = Video.query.filter_by(user_id=user_id).order_by(Video.uploaded_at.desc()).all()
    return render_template('profile.html', user=user, photos=photos, videos=videos)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.gender = form.gender.data
        current_user.birth_place = form.birth_place.data
        current_user.school = form.school.data
        current_user.hobbies = form.hobbies.data
        current_user.about = form.about.data
        current_user.current_location = form.current_location.data
        current_user.current_activity = form.current_activity.data
        
        # Handle profile photo
        # Handle profile photo
        if form.profile_photo.data:
            try:
                filename = save_uploaded_file(form.profile_photo.data, app.config['UPLOAD_FOLDER'])
                if filename:
                    current_user.profile_photo = filename
                    
                    # Create thumbnail
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', filename)
                    
                    # Ensure thumbnails directory exists
                    os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
                    
                    create_thumbnail(image_path, thumbnail_path)
                else:
                    flash('Profil fotoğrafı kaydedilemedi. Lütfen dosya formatını kontrol edin.', 'warning')
            except Exception as e:
                print(f"Profile Photo Upload Error: {str(e)}")
                flash(f'Profil fotoğrafı yüklenirken hata oluştu: {str(e)}', 'danger')
        
        db.session.commit()
        flash('Profiliniz güncellendi!', 'success')
        return redirect(url_for('profile', user_id=current_user.id))
    
    elif request.method == 'GET':
        # Pre-fill form with current data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.gender.data = current_user.gender
        form.birth_place.data = current_user.birth_place
        form.school.data = current_user.school
        form.hobbies.data = current_user.hobbies if current_user.hobbies else ''
        form.about.data = current_user.about
        form.current_location.data = current_user.current_location
        form.current_activity.data = current_user.current_activity
    
    return render_template('edit_profile.html', form=form)

@app.route('/people')
@login_required
def people():
    """List all users"""
    users = User.query.all()
    return render_template('people.html', users=users)

@app.route('/photos')
@login_required
def photos():
    """Photo gallery"""
    all_photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()
    return render_template('photos.html', photos=all_photos)

@app.route('/photos/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    """Upload photo"""
    form = PhotoUploadForm()
    
    if form.validate_on_submit():
        try:
            filename = save_uploaded_file(form.photo.data, app.config['UPLOAD_FOLDER'])
            if filename:
                photo = Photo(
                    user_id=current_user.id,
                    filename=filename,
                    caption=form.caption.data
                )
                
                # Create thumbnail
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                thumbnail_filename = f"thumb_{filename}"
                thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail_filename)
                
                # Ensure thumbnails directory exists
                os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
                
                if create_thumbnail(image_path, thumbnail_path):
                    photo.thumbnail = thumbnail_filename
                
                db.session.add(photo)
                db.session.commit()
                
                flash('Fotoğraf başarıyla yüklendi!', 'success')
                return redirect(url_for('photo_detail', photo_id=photo.id))
            else:
                flash('Dosya kaydedilemedi. Lütfen dosya formatını kontrol edin.', 'danger')
        except Exception as e:
            print(f"Upload Error: {str(e)}")
            flash(f'Fotoğraf yüklenirken bir hata oluştu: {str(e)}', 'danger')
    
    return render_template('upload_photo.html', form=form)

@app.route('/photos/<int:photo_id>')
@login_required
def photo_detail(photo_id):
    """Photo detail with tagging"""
    photo = Photo.query.get_or_404(photo_id)
    users = User.query.all()
    return render_template('photo_detail.html', photo=photo, users=users)

@app.route('/photos/<int:photo_id>/tag', methods=['POST'])
@login_required
def tag_photo(photo_id):
    """Add tag to photo"""
    photo = Photo.query.get_or_404(photo_id)
    
    data = request.get_json()
    tag = PhotoTag(
        photo_id=photo_id,
        tagged_user_id=data['user_id'],
        shape=data['shape'],
        coords=data['coords']
    )
    
    db.session.add(tag)
    db.session.commit()
    
    return jsonify({'success': True, 'tag_id': tag.id})

@app.route('/photos/<int:photo_id>/tag/<int:tag_id>', methods=['DELETE'])
@login_required
def delete_tag(photo_id, tag_id):
    tag = PhotoTag.query.get_or_404(tag_id)
    photo = Photo.query.get_or_404(photo_id)
    
    # Check permissions: user owns the photo OR user is the tagged person
    # (Assuming the person who tagged is either the photo owner or we don't track tagger separately, 
    # but usually photo owner has full control)
    if current_user.id != photo.user_id and current_user.id != tag.tagged_user_id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
        
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/videos')
@login_required
def videos():
    """Video gallery"""
    all_videos = Video.query.order_by(Video.uploaded_at.desc()).all()
    return render_template('videos.html', videos=all_videos)

@app.route('/videos/add', methods=['GET', 'POST'])
@login_required
def add_video():
    """Add YouTube video"""
    form = VideoForm()
    
    if form.validate_on_submit():
        youtube_id = extract_youtube_id(form.youtube_url.data)
        if youtube_id:
            video = Video(
                user_id=current_user.id,
                youtube_url=form.youtube_url.data,
                youtube_id=youtube_id,
                title=form.title.data,
                description=form.description.data
            )
            db.session.add(video)
            db.session.commit()
            
            flash('Video eklendi!', 'success')
            return redirect(url_for('videos'))
        else:
            flash('Geçersiz YouTube URL.', 'danger')
    
    return render_template('add_video.html', form=form)

@app.route('/forum')
@login_required
def forum():
    """Forum posts"""
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('forum.html', posts=posts)

@app.route('/forum/post', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create forum post"""
    form = ForumPostForm()
    
    if form.validate_on_submit():
        post = ForumPost(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        
        flash('Mesajınız gönderildi!', 'success')
        return redirect(url_for('forum'))
    
    return render_template('create_post.html', form=form)

@app.route('/forum/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    """View forum post and replies"""
    post = ForumPost.query.get_or_404(post_id)
    form = ForumReplyForm()
    
    if form.validate_on_submit():
        reply = ForumReply(
            post_id=post_id,
            user_id=current_user.id,
            content=form.content.data
        )
        db.session.add(reply)
        db.session.commit()
        
        flash('Yanıtınız eklendi!', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    
    return render_template('view_post.html', post=post, form=form)

@app.route('/messages')
@login_required
def messages():
    """User messages"""
    received = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.created_at.desc()).all()
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    return render_template('messages.html', received=received, sent=sent)

@app.route('/messages/send', methods=['GET', 'POST'])
@login_required
def send_message():
    """Send private message"""
    form = MessageForm()
    
    # Populate recipient choices
    users = User.query.filter(User.id != current_user.id).all()
    form.recipient.choices = [(u.id, f"{u.first_name} {u.last_name} (@{u.username})") for u in users]
    
    if form.validate_on_submit():
        message = Message(
            sender_id=current_user.id,
            recipient_id=form.recipient.data,
            subject=form.subject.data,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        
        flash('Mesajınız gönderildi!', 'success')
        return redirect(url_for('messages'))
    
    return render_template('send_message.html', form=form)

@app.route('/messages/<int:message_id>')
@login_required
def view_message(message_id):
    """View message"""
    message = Message.query.get_or_404(message_id)
    
    # Check if user is sender or recipient
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('Bu mesajı görüntüleme yetkiniz yok.', 'danger')
        return redirect(url_for('messages'))
    
    # Mark as read if recipient
    if message.recipient_id == current_user.id and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('view_message.html', message=message)

@app.route('/activity')
@login_required
def activity():
    """Who, Where, What - Activity tracking"""
    users = User.query.filter(
        (User.current_location.isnot(None)) | (User.current_activity.isnot(None))
    ).all()
    return render_template('activity.html', users=users)

@app.route('/map')
@login_required
def map_view():
    """Map with user locations"""
    all_locations = Location.query.all()
    locations_data = []
    
    for loc in all_locations:
        locations_data.append({
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'user': {
                'first_name': loc.user.first_name,
                'last_name': loc.user.last_name
            }
        })
        
    return render_template('map.html', locations=locations_data)

@app.route('/map/update', methods=['POST'])
@login_required
def update_location():
    """Update user location"""
    data = request.get_json()
    
    location = Location.query.filter_by(user_id=current_user.id).first()
    if location:
        location.latitude = data['latitude']
        location.longitude = data['longitude']
        location.address = data.get('address', '')
    else:
        location = Location(
            user_id=current_user.id,
            latitude=data['latitude'],
            longitude=data['longitude'],
            address=data.get('address', '')
        )
        db.session.add(location)
    
    db.session.commit()
    return jsonify({'success': True})

# Template filters
@app.template_filter('hobby_display')
def hobby_display(hobbies_str):
    """Display comma-separated hobbies"""
    if not hobbies_str:
        return ''
    return hobbies_str

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
