# SABİS Platformu - Ücretsiz Dağıtım Rehberi (Render.com)

Projeniz dağıtıma hazır hale getirildi. Aşağıdaki adımları izleyerek projenizi ücretsiz olarak yayınlayabilirsiniz.

## 1. GitHub'a Yükleme
Projenizin kodlarını GitHub'a yüklemeniz gerekiyor.
1. [GitHub](https://github.com) hesabınıza giriş yapın ve yeni bir repository oluşturun.
2. Terminalde şu komutları çalıştırarak kodlarınızı yükleyin:
   ```bash
   git init
   git add .
   git commit -m "İlk sürüm"
   git branch -M main
   git remote add origin <GITHUB_REPO_URL>
   git push -u origin main
   ```

## 2. Render.com Hesabı
1. [Render.com](https://render.com) adresine gidin.
2. "Get Started" diyerek GitHub hesabınızla giriş yapın.

## 3. Veritabanı Oluşturma (PostgreSQL)
1. Render panelinde **New +** butonuna basın ve **PostgreSQL** seçin.
2. **Name:** `sabis-db` (veya istediğiniz bir isim).
3. **Instance Type:** `Free` seçeneğini işaretleyin.
4. **Create Database** butonuna tıklayın.
5. Oluşturulduktan sonra **Internal Database URL** değerini kopyalayın.

## 4. Web Servisi Oluşturma
1. Render panelinde tekrar *New +** butonuna basın ve **Web Service** seçin.
2. GitHub reponuzu listeden bulup **Connect** butonuna basın.
3. Aşağıdaki ayarları yapın:
   - **Name:** `sabis-platform`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** `Free`
4. **Advanced** bölümüne tıklayın ve **Environment Variables** ekleyin:
   - `Key`: `DATABASE_URL` | `Value`: (Kopyaladığınız Internal Database URL)
   - `Key`: `SECRET_KEY` | `Value`: (Rastgele zor bir şifre yazın)
   - `Key`: `PYTHON_VERSION` | `Value`: `3.11.5`
5. **Create Web Service** butonuna tıklayın.

Tebrikler! Birkaç dakika içinde siteniz yayına girecek ve size verilen URL üzerinden erişebileceksiniz.
