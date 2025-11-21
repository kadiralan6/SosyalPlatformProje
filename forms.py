from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, RadioField, SelectMultipleField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from models import User

class RegistrationForm(FlaskForm):
    """User registration form with all required form elements"""
    
    # Basic information
    username = StringField('Kullanıcı Adı', 
                          validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('E-posta', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', 
                            validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifre Tekrar', 
                                    validators=[DataRequired(), EqualTo('password')])
    
    # Profile information
    first_name = StringField('Ad', 
                            validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Soyad', 
                           validators=[DataRequired(), Length(max=50)])
    
    # Radiobutton - Gender
    gender = RadioField('Cinsiyet', 
                       choices=[('male', 'Erkek'), ('female', 'Kadın'), ('other', 'Diğer')],
                       validators=[DataRequired()])
    
    # Combobox/Select - Birth Place
    birth_place = SelectField('Doğum Yeri',
                             choices=[
                                 ('', 'Seçiniz...'),
                                 ('istanbul', 'İstanbul'),
                                 ('ankara', 'Ankara'),
                                 ('izmir', 'İzmir'),
                                 ('bursa', 'Bursa'),
                                 ('antalya', 'Antalya'),
                                 ('adana', 'Adana'),
                                 ('other', 'Diğer')
                             ])
    
    # Combobox/Select - School
    school = SelectField('Okul',
                        choices=[
                            ('', 'Seçiniz...'),
                            ('bogazici', 'Boğaziçi Üniversitesi'),
                            ('metu', 'ODTÜ'),
                            ('itu', 'İTÜ'),
                            ('hacettepe', 'Hacettepe Üniversitesi'),
                            ('bilkent', 'Bilkent Üniversitesi'),
                            ('other', 'Diğer')
                        ])
    
    # Text input - Hobbies (comma-separated tags)
    hobbies = StringField('Hobiler',
                         validators=[Length(max=500)],
                         render_kw={'placeholder': 'Örn: Kitap okuma, Spor, Müzik, Seyahat...'})
    
    # Textarea - About
    about = TextAreaField('Hakkımda', 
                         validators=[Length(max=1000)])
    
    # File upload - Profile photo
    profile_photo = FileField('Profil Fotoğrafı',
                             validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Sadece resim dosyaları!')])
    
    submit = SubmitField('Kayıt Ol')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten kullanılıyor.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kayıtlı.')


class LoginForm(FlaskForm):
    """User login form"""
    
    username = StringField('Kullanıcı Adı', 
                          validators=[DataRequired()])
    password = PasswordField('Şifre', 
                            validators=[DataRequired()])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')


class ProfileForm(FlaskForm):
    """Profile edit form"""
    
    first_name = StringField('Ad', 
                            validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Soyad', 
                           validators=[DataRequired(), Length(max=50)])
    gender = RadioField('Cinsiyet', 
                       choices=[('male', 'Erkek'), ('female', 'Kadın'), ('other', 'Diğer')])
    birth_place = SelectField('Doğum Yeri',
                             choices=[
                                 ('', 'Seçiniz...'),
                                 ('istanbul', 'İstanbul'),
                                 ('ankara', 'Ankara'),
                                 ('izmir', 'İzmir'),
                                 ('bursa', 'Bursa'),
                                 ('antalya', 'Antalya'),
                                 ('adana', 'Adana'),
                                 ('other', 'Diğer')
                             ])
    school = SelectField('Okul',
                        choices=[
                            ('', 'Seçiniz...'),
                            ('bogazici', 'Boğaziçi Üniversitesi'),
                            ('metu', 'ODTÜ'),
                            ('itu', 'İTÜ'),
                            ('hacettepe', 'Hacettepe Üniversitesi'),
                            ('bilkent', 'Bilkent Üniversitesi'),
                            ('other', 'Diğer')
                        ])
    hobbies = StringField('Hobiler',
                         validators=[Length(max=500)],
                         render_kw={'placeholder': 'Örn: Kitap okuma, Spor, Müzik, Seyahat...'})
    about = TextAreaField('Hakkımda', 
                         validators=[Length(max=1000)])
    profile_photo = FileField('Profil Fotoğrafı',
                             validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Sadece resim dosyaları!')])
    
    # Activity tracking
    current_location = StringField('Şu Anki Konum', 
                                  validators=[Length(max=100)])
    current_activity = StringField('Ne Yapıyorum?', 
                                  validators=[Length(max=200)])
    
    submit = SubmitField('Güncelle')


class PhotoUploadForm(FlaskForm):
    """Photo upload form"""
    
    photo = FileField('Fotoğraf', 
                     validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Sadece resim dosyaları!')])
    caption = StringField('Açıklama', 
                         validators=[Length(max=500)])
    submit = SubmitField('Yükle')


class VideoForm(FlaskForm):
    """YouTube video form"""
    
    youtube_url = StringField('YouTube URL', 
                             validators=[DataRequired()])
    title = StringField('Başlık', 
                       validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Açıklama', 
                               validators=[Length(max=1000)])
    submit = SubmitField('Ekle')


class ForumPostForm(FlaskForm):
    """Forum post form"""
    
    title = StringField('Başlık', 
                       validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('İçerik', 
                           validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Gönder')


class ForumReplyForm(FlaskForm):
    """Forum reply form"""
    
    content = TextAreaField('Yanıt', 
                           validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Yanıtla')


class MessageForm(FlaskForm):
    """Private message form"""
    
    recipient = SelectField('Alıcı', 
                           coerce=int, 
                           validators=[DataRequired()])
    subject = StringField('Konu', 
                         validators=[Length(max=200)])
    content = TextAreaField('Mesaj', 
                           validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Gönder')


class LocationForm(FlaskForm):
    """Location form for map"""
    
    latitude = StringField('Enlem', 
                          validators=[DataRequired()])
    longitude = StringField('Boylam', 
                           validators=[DataRequired()])
    address = StringField('Adres', 
                         validators=[Length(max=255)])
    submit = SubmitField('Konumu Kaydet')
