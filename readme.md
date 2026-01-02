# Kütüphane Yönetim Sistemi

Bu proje, Python 202 Bootcamp kapsamında geliştirilmiş olup, kitap koleksiyonunuzu yönetmek için hem Komut Satırı Arayüzü (CLI) hem de REST API sunan bir kütüphane yönetim sistemidir. Open Library API'si ile entegre olarak, kitapları ISBN numaralarını kullanarak çevrimiçi olarak arayıp eklemenize olanak tanır. Kütüphaneniz, `library.json` dosyasında kalıcı olarak saklanır.

## Temel Özellikler

*   **Kitap Ekleme, Silme ve Listeleme:** Kütüphanenize kolayca kitap ekleyin, çıkarın ve mevcut tüm kitapları listeleyin.
*   **ISBN ile Otomatik Bilgi Çekme:** Bir kitabın ISBN'sini girdiğinizde, [Open Library API](https://openlibrary.org/developers/api)'sini kullanarak başlık ve yazar gibi bilgileri otomatik olarak alır ve kütüphanenize ekler.
*   **Kalıcı Depolama:** Kitap koleksiyonunuz, okunabilir bir JSON (`library.json`) dosyasında saklanır.
*   **Çift Arayüz:**
    *   **Komut Satırı Arayüzü (CLI):** `main.py` üzerinden çalışan, menü tabanlı ve kullanımı kolay bir arayüz.
    *   **REST API:** FastAPI ile oluşturulmuş, modern ve tam özellikli bir web arayüzü. Swagger/OpenAPI dokümantasyonu ile birlikte gelir.
*   **Asenkron İşlemler:** Ağ istekleri (`httpx` kullanılarak) asenkron olarak yönetilir.
*   **Kapsamlı Testler:** `pytest` kullanılarak yazılmış birim ve entegrasyon testleri içerir.

## Kullanılan Teknolojiler

*   **Dil:** Python 3.8+
*   **Web Çerçevesi (API):** [FastAPI](https://fastapi.tiangolo.com/)
*   **HTTP İstemcisi:** [httpx](https://www.python-httpx.org/)
*   **Test:** [pytest](https://docs.pytest.org/) ve [pytest-asyncio](https://pypi.org/project/pytest-asyncio/)
*   **API Sunucusu:** [Uvicorn](https://www.uvicorn.org/)

## Kurulum

**1. Repoyu Klonlama:**
```bash
git clone <proje-repo-url>
cd <proje-dizini>
```

**2. Sanal Ortam Oluşturma ve Aktive Etme:**
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Bağımlılıkları Yükleme:**
```bash
pip install -r requirements.txt
```

## Kullanım (Usage)

### 1. Komut Satırı Arayüzü (CLI)
Terminal üzerinden interaktif menü ile kütüphanenizi yönetmek için `main.py` dosyasını çalıştırın.

```bash
python main.py
```

### 2. REST API Sunucusu
Web tabanlı arayüz üzerinden kütüphaneyi yönetmek için FastAPI sunucusunu başlatın.

```bash
uvicorn api:app --reload
```
Sunucu başlatıldığında, `http://1227.0.0.1:8000` adresinde çalışacaktır.

## API Dokümantasyonu (Endpoints)

API'nin interaktif dokümantasyonuna [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresinden ulaşabilirsiniz.

### `GET /books`
*   **Açıklama:** Kütüphanedeki tüm kitapları listeler.
*   **Başarılı Cevap (200 OK):**
    ```json
    [
      {
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "9780441172719"
      }
    ]
    ```

### `POST /books`
*   **Açıklama:** Verilen ISBN'ye sahip bir kitabı Open Library'den arar ve kütüphaneye ekler.
*   **İstek Gövdesi (Request Body):**
    ```json
    {
      "isbn": "9780441172719"
    }
    ```
*   **Başarılı Cevap (200 OK):** Eklenen kitabın bilgilerini döndürür.
*   **Başarısız Cevap (404 Not Found):** Kitap bulunamazsa hata mesajı döndürür.

### `DELETE /books/{isbn}`
*   **Açıklama:** Belirtilen ISBN'ye sahip kitabı kütüphaneden kaldırır.
*   **URL Parametresi:** `isbn` (Örn: `/books/9780441172719`)
*   **Başarılı Cevap (200 OK):**
    ```json
    {
      "detail": "Book removed"
    }
    ```
*   **Başarısız Cevap (404 Not Found):** Kitap bulunamazsa hata mesajı döndürür.

## Testler

Projenin testlerini çalıştırmak için ana dizinde aşağıdaki komutu çalıştırın:
```bash
pytest
```
