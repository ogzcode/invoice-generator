# Backend — json_process.py Teknik Dokümantasyonu

Bu dosya `backend/json_process.py` içindeki fonksiyonların, akışın ve kullanımın teknik özetini içerir. Amaç: JSON tabanlı şablon tanımından (ve isteğe bağlı veri nesnesinden) pozisyonlanmış HTML çıktısı üretmektir (fatura/etiket/şablon önizlemesi).

## Dosyalar

- `backend/json_process.py` — ana işlem kütüphanesi.
- `backend/test.json` — örnek JSON şablon (proje kökünde).
- `backend/requirements.txt` — gerekli Python paketleri (ör. `beautifulsoup4`).

## Amaç ve Genel Akış

- JSON dosyası okunur (`load_json_content`).
- Temel HTML şablonu oluşturulur (`create_base_html_template`).
- `pageItems` içindeki öğeler tiplerine göre HTML elemanları üretilir (`create_text_element`, `create_data_element`, `create_table_element`, `create_image_element`).
- Üretilen HTML, `BeautifulSoup` ile parse edilip tabloların gerçek yüksekliğine göre alt öğelerin `top` pozisyonları düzeltilir (`adjust_elements_after_table_processing`).
- Son HTML dosyaya yazılır (`process_json_to_html`) veya sadece şablon kaydedilir (`save_template_html`).

## Hızlı Kurulum (Windows / PowerShell)

1. Sanal ortam oluşturun ve aktif edin:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Bağımlılıkları yükleyin:

```powershell
pip install -r requirements.txt
```

> Not: `requirements.txt` içinde `beautifulsoup4` olmalıdır.

## Programatik Kullanım Örnekleri

- Basit kullanım (HTML üretme ve kaydetme):

```python
from json_process import process_json_to_html

data = {
    # Şablonunuzdaki data anahtarları burada yer alır
}

process_json_to_html('test.json', data, 'out.html')
```

- Sadece şablon (veri olmadan):

```python
from json_process import save_template_html

save_template_html('test.json', 'template.html')
```

## Fonksiyon Referansı (kısa)

- `load_json_content(file_path)` — UTF-8 ile JSON okur ve dict döner.
- `create_base_html_template(page_size='A4')` — temel HTML/CSS şablonu döner.
- `get_nested_value(data, key)` — nokta ayrılmış anahtarla iç içe dict'e erişir (`'user.name'`).
- `create_text_element(item, data=None)` — sabit metin elemanı oluşturur.
- `create_data_element(item, data=None)` — `item['value']` anahtarıyla `data` içinde değer bulup gösterir.
- `create_table_element(item, data=None)` — `dataColumns` veya varsayılan başlıklarla tablo oluşturur; `item['value']` altında list veri bekler.
- `create_image_element(item, data=None)` — veri olarak verilen URL yoksa placeholder gösterir.
- `generate_html_from_json(json_data, data=None)` — tüm öğeleri birleştirip HTML üretir.
- `adjust_elements_after_table_processing(soup, json_data)` — tablo gerçek yüksekliğine göre alt öğelerin `top` stilini kaydırır.
- `process_json_to_html(json_file_path, data, output_path)` — tam iş akışı: dosyadan JSON al, HTML üret, post-process, kaydet.
- `save_template_html(json_file_path, output_path)` — veri olmadan şablon oluşturup kaydeder.

## Bilinen Sınırlamalar ve Güvenlik Notları

- HTML kaçışı uygulanmıyor: `item['value']` ve veri içerikleri doğrudan HTML içine yazılıyor. Eğer kullanıcı kaynaklı veri varsa `html.escape()` benzeri kaçış/temizleme ekleyin (XSS riski).
- `adjust_elements_after_table_processing` içindeki `row_height = 34` ve `+40` header offset sabitleridir; dinamik/temaya bağlı değişiklikler için parametre yapılmalıdır.
- `re.sub` ile `top: Npx` deseni değiştirilir; farklı stil formatlarında/ünitelerde çalışmayabilir.
- `create_table_element` içinde gövde hücreleri hep `text-align:left` ile render ediliyor; kolon bazlı hizalama (`dataColumns[].textAlign`) body hücrelerine yansıtılmıyor.
- `data-key` olarak kullanılan `item['value']` alanının benzersiz olması bekleniyor; çakışma varsa post-process yanlış elemanları güncelleyebilir.

## Öneriler / Geliştirme Adımları

- HTML kaçış: tüm veri çıktılarında `html.escape()` uygulayın.
- Parametrize edin: `row_height` ve header offset değerlerini JSON `item` veya global konfig üzerinden alın.
- Tablo hücre hizalamasını düzeltin: `td`'lere header hizalamasını uygulayın.
- Benzersiz id: öğelere `data-id` veya `id` alanı ekleyip post-process'te bu alanı kullanın.
- Hata yönetimi: dosya okuma/parsing ve BS4 işlemlerini `try/except` ile sarmalayın ve `logging` kullanın.
- Testler: `get_nested_value`, `create_table_element`, `adjust_elements_after_table_processing` için birim testleri ekleyin.

## Örnek CLI (hızlı)

```powershell
python -c "from json_process import process_json_to_html; process_json_to_html('test.json', {}, 'out.html')"
```

---

Bu döküman `backend/json_process.py` için teknik özet, kullanım ve geliştirme önerilerini içerir. İsterseniz bu README'yi genişletip örnek JSON girdileri ve bir test harness ekleyebilirim.
