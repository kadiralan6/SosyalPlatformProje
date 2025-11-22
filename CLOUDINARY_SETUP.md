# Cloudinary Kurulum Rehberi

## 1. Cloudinary Hesabı Oluşturma

1. [Cloudinary'ye kaydolun](https://cloudinary.com/users/register_free)
2. Email adresinizi doğrulayın
3. Dashboard'a giriş yapın

## 2. API Bilgilerini Alma

Dashboard'da **Product Environment Credentials** bölümünde şu bilgileri bulacaksınız:
- **Cloud Name**
- **API Key**
- **API Secret**

Bu bilgileri not edin.

## 3. Render'da Environment Variables Ekleme

1. Render Dashboard'da projenize gidin
2. **Environment** sekmesine tıklayın
3. Şu değişkenleri ekleyin:
   - `Key`: `CLOUDINARY_CLOUD_NAME` | `Value`: (Cloud Name değeriniz)
   - `Key`: `CLOUDINARY_API_KEY` | `Value`: (API Key değeriniz)
   - `Key`: `CLOUDINARY_API_SECRET` | `Value`: (API Secret değeriniz)
4. **Save Changes** butonuna tıklayın

## 4. GitHub'a Yükleme ve Deploy

1. Değişiklikleri GitHub'a yükleyin:
   ```bash
   git add .
   git commit -m "Add Cloudinary integration for persistent file storage"
   git push
   ```

2. Render otomatik olarak yeni kodu çekip deploy edecek

## 5. Test Etme

Deploy tamamlandıktan sonra:
1. Siteye giriş yapın
2. Profil fotoğrafı yükleyin
3. Fotoğraf galerisi sayfasından fotoğraf yükleyin
4. Servisi yeniden başlatın (Render Dashboard → Manual Deploy → Deploy latest commit)
5. Resimlerin hala orada olduğunu doğrulayın ✅

## Artık Resimler Kalıcı!

Cloudinary sayesinde:
- ✅ Resimler deploy sonrası silinmeyecek
- ✅ Servis yeniden başlatılsa bile resimler kaybolmayacak
- ✅ Otomatik thumbnail oluşturma
- ✅ Otomatik optimizasyon (boyut, kalite)
- ✅ 25GB ücretsiz depolama
