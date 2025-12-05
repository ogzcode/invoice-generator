from bs4 import BeautifulSoup
import json
import re

fake_date = {
    "invoiceName": "INV-1001",
    "image": "./image.png",
    "table": [
        {
            "productName": "Widget A",
            "unitPrice": 10,
            "vatRate": 0.2,
            "totalAmount": 12
        },
        {
            "productName": "Widget B",
            "unitPrice": 10,
            "vatRate": 0.2,
            "totalAmount": 12
        },
        {
            "productName": "Widget C",
            "unitPrice": 10,
            "vatRate": 0.2,
            "totalAmount": 12
        },
        {
            "productName": "Widget D",
            "unitPrice": 10,
            "vatRate": 0.2,
            "totalAmount": 12
        },
        {
            "productName": "Widget E",
            "unitPrice": 10,
            "vatRate": 0.2,
            "totalAmount": 12
        },
        {
            "productName": "Widget F",
            "unitPrice": 20,
            "vatRate": 0.18,
            "totalAmount": 23.6
        },
        {
            "productName": "Widget G",
            "unitPrice": 15,
            "vatRate": 0.2,
            "totalAmount": 18
        },
        {
            "productName": "Widget H",
            "unitPrice": 25,
            "vatRate": 0.2,
            "totalAmount": 30
        },
        {
            "productName": "Widget I",
            "unitPrice": 12,
            "vatRate": 0.2,
            "totalAmount": 14.4
        },
        {
            "productName": "Widget J",
            "unitPrice": 18,
            "vatRate": 0.2,
            "totalAmount": 21.6
        }
    ],
    "totalVat": 25,
    "total": 165
}


def load_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_nested_value(data, key):
    """İç içe verileri anahtardan erişir. Örn: "user.name" -> data["user"]["name"]"""
    keys = key.split(".")
    value = data
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return None
    return value


def process_text_element(element, data):
    """Text tipi elementi işle"""
    data_key = element.get("data-key")
    if data_key and data_key in data:
        element.string = str(data[data_key])


def process_data_element(element, data):
    """Data tipi elementi işle"""
    data_key = element.get("data-key")
    if data_key:
        value = get_nested_value(data, data_key)
        if value is not None:
            element.string = str(value)


def process_table_element(element, data):
    """Table tipi elementi işle"""
    data_key = element.get("data-key")
    table = element.find("table")
    
    if not table or not data_key or data_key not in data:
        return
    
    table_data = data[data_key]
    if not isinstance(table_data, list):
        return
    
    # Thead'den header bilgisini al
    thead = table.find("thead")
    if not thead:
        thead = table.find("tr")  # İlk tr varsa header olarak kullan
    
    headers = []
    if thead:
        for th in thead.find_all("th"):
            key = th.get("data-key")
            if key:
                headers.append(key)
    
    # Tbody bulup satırları temizle
    tbody = table.find("tbody")
    if tbody:
        tbody.clear()
    else:
        tbody = BeautifulSoup("<tbody></tbody>", "html.parser").tbody
        table.append(tbody)
    
    # Veri satırlarını ekle
    for row_data in table_data:
        tr = BeautifulSoup("<tr></tr>", "html.parser").tr
        
        for header_key in headers:
            td = BeautifulSoup(
                f'<td style="border:1px solid #d1d5db;padding:8px;text-align:left"></td>',
                "html.parser"
            ).td
            value = row_data.get(header_key, "")
            td.string = str(value)
            tr.append(td)
        
        tbody.append(tr)


def process_image_element(element, data):
    """Image tipi elementi işle"""
    data_key = element.get("data-key")
    if data_key and data_key in data:
        image_url = data[data_key]
        if image_url:
            # Mevcut img tag'ını bul ya da oluştur
            img = element.find("img")
            if not img:
                img = BeautifulSoup(f'<img src="{image_url}" style="width:100%;height:100%;object-fit:cover;"/>', "html.parser").img
                element.clear()
                element.append(img)
            else:
                img["src"] = image_url
        else:
            # Boş image_url ise placeholder'ı koru
            pass


def calculate_row_height(row_element):
    """Tablo satırının yüksekliğini hesapla"""
    if not row_element:
        return 0
    
    cells = row_element.find_all(['td', 'th'])
    if not cells:
        return 0
    
    # CSS'den padding ve border bilgisini al
    # Varsayılan: 8px padding + 1px border (toplam ~18px per row)
    return 34  # 8px padding top + 8px padding bottom + 1px border top + 1px border bottom


def adjust_element_positions(soup, table_element, original_table_height):
    """Tablo yüksekliği değişirse, altındaki elementlerin Y konumunu ayarla"""
    if not table_element or not table_element.find("table"):
        return
    
    table = table_element.find("table")
    tbody = table.find("tbody")
    
    if not tbody:
        return
    
    rows = tbody.find_all("tr")
    actual_height = len(rows) * calculate_row_height(rows[0] if rows else None)
    
    # Orijinal yüksekliği string'den çıkar (örn: "90px" -> 90)
    try:
        original_height = int(original_table_height.replace("px", "").replace("mm", ""))
    except:
        original_height = 90
    
    # Fark hesapla
    height_difference = actual_height - original_height
    
    if height_difference <= 0:
        return  # Tablo küçüldü, ayarlama gerekli yok
    
    # Tablo elementinin style'ından top ve height'ını al
    table_style = table_element.get("style", "")
    table_top = 0
    
    # Style'den top pozisyonunu çıkar
    import re
    top_match = re.search(r'top:\s*(\d+)px', table_style)
    if top_match:
        table_top = int(top_match.group(1))
    
    # Tablo elementinin sonrası gelen tüm elementleri bul
    all_items = soup.find_all(class_="item")
    for item in all_items:
        # Tablo elementinin sonrası gelen elementleri kontrol et
        item_style = item.get("style", "")
        
        # Style'den top değerini çıkar
        top_match = re.search(r'top:\s*(\d+)px', item_style)
        if not top_match:
            continue
        
        item_top = int(top_match.group(1))
        
        # Eğer bu element tablo altında ise (top pozisyonu tablo altında)
        table_bottom = table_top + original_height
        if item_top >= table_bottom:
            # Yeni top konumunu hesapla
            new_top = item_top + height_difference
            new_style = re.sub(r'top:\s*\d+px', f'top: {new_top}px', item_style)
            item["style"] = new_style


def process_html(html_content, data):
    """HTML'yi BeautifulSoup ile parse et ve verileri yerleştir"""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Tüm item elementlerini bul
    items = soup.find_all(class_="item")
    
    for item in items:
        data_type = item.get("data-type")
        original_height = item.get("style", "")
        
        if data_type == "text":
            process_text_element(item, data)
        elif data_type == "data":
            process_data_element(item, data)
        elif data_type == "table":
            # Orijinal yüksekliği kaydet
            height_match = re.search(r'height:\s*(\d+px)', original_height)
            original_table_height = height_match.group(1) if height_match else "90px"
            
            process_table_element(item, data)
            adjust_element_positions(soup, item, original_table_height)
        elif data_type == "image":
            process_image_element(item, data)
    
    return str(soup)


def save_html(html_content, output_path):
    """İşlenen HTML'yi dosyaya yaz"""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Çıktı dosyası kaydedildi: {output_path}")


def main():
    # HTML şablonunu yükle
    html_template = load_file_content("./example.html")
    
    # HTML'yi işle
    processed_html = process_html(html_template, fake_date)
    
    # Sonucu dosyaya yaz
    save_html(processed_html, "./processed_invoice.html")
    
    print("İşlem tamamlandı!")


if __name__ == "__main__":
    main()
