# Fatura İşleme Sistemi - Yeni Yapı

Bu proje modüler bir yapıya dönüştürülmüştür. Her sınıf kendi özel görevine odaklanır.

## 📁 Dosya Yapısı

### 🏗️ Ana Dosyalar
- `invoice_processor.py` - Ana koordinatör sınıf
- `main.py` - API entegrasyonu ve kullanıcı arayüzü

### 🔧 Modüler Sınıflar

#### `currency_manager.py` - Para Birimi Yönetimi
- Para birimi kodlarını yönetir
- Para formatlaması yapar
- Sayıları Türkçe yazıya çevirir
- **Sorumluluklar:**
  - Currency.json dosyasını yükler
  - Para birimlerini formatlar
  - Rakamları yazıya çevirir

#### `tax_manager.py` - Vergi Hesaplamaları
- Tüm vergi hesaplamalarını yapar
- Vergi kodlarına göre hesaplama
- Tevkifat, KDV, ÖTV hesaplamaları
- **Sorumluluklar:**
  - Taxes.json dosyasını yükler
  - Vergi oranlarını hesaplar
  - Toplam vergi tutarlarını bulur

#### `html_processor.py` - HTML İşlemeleri
- HTML dosyasını düzenler
- Tablo oluşturur ve yerleştirir
- Element pozisyonlarını ayarlar
- **Sorumluluklar:**
  - BeautifulSoup ile HTML manipülasyonu
  - Dinamik tablo oluşturma
  - CSS pozisyonlarını ayarlama

#### `data_mapper.py` - Veri Haritalama
- JSON verisini HTML elementlerine eşler
- Ana fatura alanları ve ürün tablosu mapping'i
- **Sorumluluklar:**
  - Data-key eşleştirmeleri
  - Lambda fonksiyonları ile veri çevirimi

#### `utils.py` - Yardımcı Fonksiyonlar
- Genel kullanım fonksiyonları
- Null kontrolü, tarih formatı vb.
- **Sorumluluklar:**
  - Güvenli veri alma
  - Tarih formatlaması
  - İndirim formatlaması

## 🎯 Avantajlar

### 1. **Tek Sorumluluk Prensibi (SRP)**
- Her sınıf sadece bir görevi yapıyor
- Kod daha anlaşılır ve bakımı kolay

### 2. **Modüler Yapı**
- Her modül bağımsız çalışabilir
- Yeni özellikler kolayca eklenebilir
- Test edilmesi daha kolay

### 3. **Okunabilirlik**
- Kodun ne yaptığı daha açık
- Her dosya küçük ve odaklanmış
- Dokümantasyon daha iyi

### 4. **Bakım Kolaylığı**
- Bir alanda değişiklik diğerlerini etkilemiyor
- Hata ayıklama daha kolay
- Genişletme daha güvenli

### 5. **Yeniden Kullanılabilirlik**
- Her modül farklı projelerde kullanılabilir
- Bağımlılıklar minimuma indirildi

## 🚀 Kullanım

```python
from invoice_processor import InvoiceProcessor

# Basit kullanım
processor = InvoiceProcessor()
result = processor.process_invoice_html(html_template, invoice_data)
```

## 📦 Gerekli Paketler
- beautifulsoup4
- requests (sadece main.py için)

## 🧪 Test
Test etmek için: `python test_refactored.py`