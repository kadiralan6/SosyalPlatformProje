# SABİS Platform

Üniversite sınıfı için sosyal ağ ve mezunlar platformu.

## Özellikler

- ✅ Kullanıcı kayıt ve giriş sistemi
- ✅ Profil yönetimi (fotoğraf, kişisel bilgiler)
- ✅ Fotoğraf yükleme ve etiketleme (HTML image map)
- ✅ YouTube video entegrasyonu
- ✅ Forum sistemi
- ✅ Özel mesajlaşma
- ✅ Aktivite takibi (Kim, Nerede, Ne Yapıyor?)
- ✅ Harita entegrasyonu (Google Maps)

## Teknoloji Yığını

- **Backend:** Python 3.x + Flask
- **Veritabanı:** PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Şablon Motoru:** Jinja2
- **Form İşleme:** Flask-WTF
- **Kimlik Doğrulama:** Flask-Login

## Kurulum

### 1. Gereksinimler

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### 2. Sanal Ortam Oluşturma

```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# veya
.venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Veritabanı Oluşturma

```bash
# PostgreSQL'e bağlan
psql -U postgres

# Veritabanı oluştur
CREATE DATABASE sabis_db;

# Kullanıcı oluştur (opsiyonel)
CREATE USER sabis_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE sabis_db TO sabis_user;
```

### 5. Environment Variables

`.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost/sabis_db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### 6. Veritabanını Başlatma

```bash
python init_db.py
```

Bu komut:
- Tüm tabloları oluşturur
- Admin kullanıcısı ekler (username: admin, password: admin123)

### 7. Uygulamayı Çalıştırma

```bash
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## Kullanım

### İlk Giriş

1. Tarayıcınızda `http://localhost:5000` adresine gidin
2. "Kayıt Ol" butonuna tıklayın
3. Formu doldurun (tüm form elemanları: radiobutton, checkbox, select, textarea, file upload)
4. Kayıt olduktan sonra giriş yapın

### Özellikler

#### Profil Yönetimi
- Profil fotoğrafı yükleme
- Kişisel bilgileri düzenleme
- Hobiler, okul, doğum yeri gibi bilgileri ekleme

#### Fotoğraflar
- Fotoğraf yükleme
- Fotoğraflarda kişi etiketleme (HTML image map - rect shape, coords)
- Thumbnail görünümü

#### Videolar
- YouTube video URL'i ile video ekleme
- Video gömme (embed)

#### Forum
- Genel mesaj gönderme
- Mesajlara yanıt verme

#### Mesajlaşma
- Kullanıcılar arası özel mesajlaşma
- Gelen/giden mesajlar

#### Aktivite
- "Kim, Nerede, Ne Yapıyor?" tablosu
- Kullanıcı aktivitelerini görüntüleme

#### Harita
- Google Maps entegrasyonu
- Kullanıcı konumlarını görüntüleme
- Konum ekleme

## Proje Yapısı

```
SosyalPlatform/
├── app.py                 # Ana Flask uygulaması
├── models.py             # Veritabanı modelleri
├── forms.py              # Form tanımlamaları
├── config.py             # Konfigürasyon
├── utils.py              # Yardımcı fonksiyonlar
├── init_db.py            # Veritabanı başlatma
├── requirements.txt      # Python bağımlılıkları
├── .env.example          # Environment variables örneği
├── .gitignore           # Git ignore
├── static/
│   ├── css/
│   │   └── style.css    # Ana stil dosyası
│   ├── js/
│   │   ├── main.js      # Ana JavaScript
│   │   └── photo-tagger.js  # Fotoğraf etiketleme
│   └── uploads/         # Kullanıcı yüklemeleri
└── templates/
    ├── base.html        # Ana şablon
    ├── index.html       # Anasayfa
    ├── register.html    # Kayıt
    ├── login.html       # Giriş
    ├── profile.html     # Profil
    ├── edit_profile.html # Profil düzenleme
    ├── people.html      # Kişiler
    ├── photos.html      # Fotoğraflar
    ├── upload_photo.html # Fotoğraf yükleme
    ├── photo_detail.html # Fotoğraf detay
    ├── videos.html      # Videolar
    ├── add_video.html   # Video ekleme
    ├── forum.html       # Forum
    ├── create_post.html # Mesaj oluşturma
    ├── view_post.html   # Mesaj görüntüleme
    ├── messages.html    # Mesajlar
    ├── send_message.html # Mesaj gönderme
    ├── view_message.html # Mesaj görüntüleme
    ├── activity.html    # Aktivite
    └── map.html         # Harita
```

## Ödev Gereksinimleri

Bu proje aşağıdaki ödev gereksinimlerini karşılar:

### Form Elemanları
- ✅ Radiobutton (Cinsiyet seçimi)
- ✅ Checkbox (Hobiler)
- ✅ Combobox/Select (Doğum yeri, Okul)
- ✅ Textarea (Hakkımda, Mesajlar)
- ✅ File Upload (Profil fotoğrafı, Fotoğraflar)

### Özellikler
- ✅ Kişi kayıt sistemi
- ✅ Oturum açma
- ✅ Forum (ortak mesajlaşma)
- ✅ Kişiler arası mesajlaşma
- ✅ Fotoğraf yükleme ve etiketleme (HTML image map - coords, shape)
- ✅ Thumbnail resimleri
- ✅ YouTube video gömme
- ✅ Tablo formatında listeleme (Kim, Nerede, Ne Yapıyor?)
- ✅ Harita entegrasyonu

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
