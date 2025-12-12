import json
from bs4 import BeautifulSoup
import re


def load_json_content(file_path):
    """JSON dosyasını yükle"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_base_html_template(page_size="A4"):
    """Temel HTML şablonunu oluştur"""
    html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Invoice</title>
  <style>
    .preview-container {{
      overflow: auto;
      padding: 20px;
      display: flex;
      justify-content: center;
    }}

    .page {{
      width: 210mm;
      min-height: 297mm;
      background: white;
      position: relative;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      margin: 0 auto;
    }}

    .item {{
      position: absolute;
      line-height: 1.5;
    }}

    /* Tablo stilleri */
    .min-w-full {{
      width: 100%;
    }}

    .border-collapse {{
      border-collapse: collapse;
    }}

    .border {{
      border-width: 1px;
    }}

    .border-gray-300 {{
      border-color: #d1d5db;
    }}

    .px-4 {{
      padding-left: 1rem;
      padding-right: 1rem;
    }}

    .py-2 {{
      padding-top: 0.5rem;
      padding-bottom: 0.5rem;
    }}

    .text-gray-700 {{
      color: #374151;
    }}

    .text-center {{
      text-align: center;
    }}

    @media print {{
      .preview-container {{
        padding: 0;
      }}

      .page {{
        margin: 0;
        padding: 20px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
        box-shadow: none;
      }}
    }}
  </style>
</head>
<body>
  <div class="preview-container">
    <div class="page">
      <!-- CONTENT_PLACEHOLDER -->
    </div>
  </div>
</body>
</html>"""
    return html_template


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


def create_text_element(item, data=None):
    """Text tipi element oluştur - veriyle birlikte"""
    pos = item["position"]
    size = item["size"]
    
    style = f"""
        position: absolute;
        left: {pos["x"]}px;
        top: {pos["y"]}px;
        width: {size["width"]}px;
        height: {size["height"]}px;
        font-family: {item["fontFamily"]};
        font-size: {item["fontSize"]}px;
        color: #000;
        text-align: {item["textAlign"]};
        font-weight: {item["fontWeight"]};
        font-style: {item["fontStyle"]};
        text-decoration: {item["textDecoration"]};
        line-height: 1.5;
    """
    
    # Text elemanları sabit metin gösterir
    content = item["value"]
    
    return f'''<div class="item" data-type="text" data-key="{item["value"]}" style="{style.strip()}">
        {content}
    </div>'''


def create_data_element(item, data=None):
    """Data tipi element oluştur - veriyle birlikte"""
    pos = item["position"]
    size = item["size"]
    
    style = f"""
        position: absolute;
        left: {pos["x"]}px;
        top: {pos["y"]}px;
        width: {size["width"]}px;
        height: {size["height"]}px;
        font-family: {item["fontFamily"]};
        font-size: {item["fontSize"]}px;
        color: #000;
        text-align: {item["textAlign"]};
        font-weight: {item["fontWeight"]};
        font-style: {item["fontStyle"]};
        text-decoration: {item["textDecoration"]};
        line-height: 1.5;
    """
    
    # Veriyi al ve yerleştir
    content = item["value"]
    if data:
        value = get_nested_value(data, item["value"])
        if value is not None:
            content = str(value)
    
    return f'''<div class="item" data-type="data" data-key="{item["value"]}" style="{style.strip()}">
        {content}
    </div>'''


def create_table_element(item, data=None):
    """Table tipi element oluştur - veriyle birlikte"""
    pos = item["position"]
    size = item["size"]
    
    style = f"""
        position: absolute;
        left: {pos["x"]}px;
        top: {pos["y"]}px;
        width: {size["width"]}px;
        height: {size["height"]}px;
        font-family: {item["fontFamily"]};
        font-size: {item["fontSize"]}px;
        color: #000;
        text-align: {item["textAlign"]};
        font-weight: {item["fontWeight"]};
        font-style: {item["fontStyle"]};
        text-decoration: {item["textDecoration"]};
        line-height: 1.5;
    """
    
    # Tablo header'larını oluştur
    headers_html = ""
    headers = []
    if "dataColumns" in item and item["dataColumns"]:
        for col in item["dataColumns"]:
            col_width = col.get("width", 120)
            col_align = col.get("textAlign", "left")
            headers.append(col["value"])
            headers_html += f'''
            <th data-key="{col["value"]}" style="border:1px solid #d1d5db;padding:8px;text-align:{col_align};width:{col_width}px">{col["label"]}</th>'''
    else:
        # Varsayılan başlık
        headers = ["productName", "unitPrice", "vatRate", "totalAmount"]
        headers_html = '''
            <th data-key="productName" style="border:1px solid #d1d5db;padding:8px;text-align:left;width:120px">Ürün Adı</th>
            <th data-key="unitPrice" style="border:1px solid #d1d5db;padding:8px;text-align:left;width:120px">Birim Fiyat</th>
            <th data-key="vatRate" style="border:1px solid #d1d5db;padding:8px;text-align:left;width:120px">KDV</th>
            <th data-key="totalAmount" style="border:1px solid #d1d5db;padding:8px;text-align:left;width:120px">Toplam</th>'''
    
    # Tablo body'sini oluştur
    tbody_html = ""
    if data and item["value"] in data:
        table_data = data[item["value"]]
        if isinstance(table_data, list):
            for row_data in table_data:
                tbody_html += "<tr>"
                for header_key in headers:
                    value = row_data.get(header_key, "")
                    tbody_html += f'<td style="border:1px solid #d1d5db;padding:8px;text-align:left">{str(value)}</td>'
                tbody_html += "</tr>"
    
    # Eğer veri yoksa boş satır ekle
    if not tbody_html:
        tbody_html = "<tr>"
        for _ in headers:
            tbody_html += '<td style="border:1px solid #d1d5db;padding:8px;text-align:left"></td>'
        tbody_html += "</tr>"
    
    table_html = f'''
        <table style="border-collapse:collapse;width:100%;min-width:100%">
          <tr>{headers_html}
          </tr>
          <tbody>
            {tbody_html}
          </tbody>
        </table>'''
    
    return f'''<div class="item" data-type="table" data-key="{item["value"]}" style="{style.strip()}">
        {table_html}
    </div>'''


def create_image_element(item, data=None):
    """Image tipi element oluştur - veriyle birlikte"""
    pos = item["position"]
    size = item["size"]
    
    style = f"""
        position: absolute;
        left: {pos["x"]}px;
        top: {pos["y"]}px;
        width: {size["width"]}px;
        height: {size["height"]}px;
        font-family: {item["fontFamily"]};
        font-size: {item["fontSize"]}px;
        color: #000;
        text-align: {item["textAlign"]};
        font-weight: {item["fontWeight"]};
        font-style: {item["fontStyle"]};
        text-decoration: {item["textDecoration"]};
        line-height: 1.5;
    """
    
    # Veriyi kontrol et
    image_url = ""
    if data and item["value"] in data:
        image_url = data[item["value"]]
    
    if image_url:
        # Gerçek resim
        content_html = f'<img src="{image_url}" style="width:100%;height:100%;object-fit:cover;"/>'
    else:
        # Placeholder image
        content_html = f'''
        <div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;">
          <div
            style="width:100%;height:100%;background:#f1f5f9;border:1px dashed #d1d5db;border-radius:6px;display:flex;align-items:center;justify-content:center;">
            <svg width="20" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
              <rect x="3" y="3" width="18" height="14" rx="1.5" stroke="#6b7280" stroke-width="1.2" fill="none" />
              <circle cx="8" cy="8" r="1.5" fill="#6b7280" />
              <path d="M3 17l5-6 4 5 3-4 6 6" stroke="#6b7280" stroke-width="1.2" fill="none" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
          </div>
        </div>'''
    
    return f'''<div class="item" data-type="image" data-key="{item["value"]}" style="{style.strip()}">
        {content_html}
    </div>'''


def generate_html_from_json(json_data, data=None):
    """JSON'dan veriyle birlikte HTML oluştur"""
    page_size = json_data.get("pageSize", "A4")
    page_items = json_data.get("pageItems", [])
    
    # Temel HTML şablonunu oluştur
    html_template = create_base_html_template(page_size)
    
    # Elementleri veriyle birlikte oluştur
    elements_html = ""
    
    for item in page_items:
        item_type = item.get("type", "text")
        
        if item_type == "text":
            elements_html += create_text_element(item, data) + "\n\n"
        elif item_type == "data":
            elements_html += create_data_element(item, data) + "\n\n"
        elif item_type == "table":
            elements_html += create_table_element(item, data) + "\n\n"
        elif item_type == "image":
            elements_html += create_image_element(item, data) + "\n\n"
    
    # Placeholder'ı elementlerle değiştir
    html_template = html_template.replace("<!-- CONTENT_PLACEHOLDER -->", elements_html)
    
    return html_template


def generate_html_template_only(json_data):
    """JSON'dan sadece şablon HTML oluştur (veri olmadan)"""
    return generate_html_from_json(json_data, None)


def adjust_elements_after_table_processing(soup, json_data):
    """Tablo işleme sonrası elementlerin konumlarını ayarla"""
    # JSON'dan tablo elementlerini bul
    page_items = json_data.get("pageItems", [])
    
    for item in page_items:
        if item.get("type") == "table":
            # Bu tablo elementinin HTML'deki karşılığını bul
            table_elements = soup.find_all("div", {"data-type": "table", "data-key": item["value"]})
            
            if not table_elements:
                continue
                
            table_element = table_elements[0]
            table = table_element.find("table")
            
            if not table:
                continue
            
            # Tablo verilerini kontrol et
            tbody = table.find("tbody")
            if not tbody:
                continue
            
            rows = tbody.find_all("tr")
            if not rows:
                continue
            
            # Orijinal yükseklik (JSON'dan)
            original_height = item["size"]["height"]
            
            # Gerçek yükseklik (satır sayısına göre)
            row_height = 34  # padding + border
            actual_height = len(rows) * row_height + 40  # header için extra
            
            # Yükseklik farkı
            height_difference = actual_height - original_height
            
            if height_difference <= 0:
                continue
            
            # Tablo konumu
            table_x = item["position"]["x"]
            table_y = item["position"]["y"]
            table_bottom = table_y + original_height
            
            # Altındaki elementleri bul ve konumlarını ayarla
            for other_item in page_items:
                other_y = other_item["position"]["y"]
                
                # Bu element tablo altında mı?
                if other_y >= table_bottom and other_item["id"] != item["id"]:
                    # HTML'deki karşılığını bul
                    other_elements = soup.find_all("div", {"data-key": other_item["value"]})
                    
                    for other_element in other_elements:
                        style = other_element.get("style", "")
                        
                        # Yeni top konumunu hesapla
                        new_top = other_y + height_difference
                        
                        # Style'da top değerini güncelle
                        new_style = re.sub(r'top:\s*\d+px', f'top: {new_top}px', style)
                        other_element["style"] = new_style


def process_json_to_html(json_file_path, data, output_path):
    """JSON dosyasından veriyle birlikte doğrudan HTML oluştur"""
    # JSON'u yükle
    json_data = load_json_content(json_file_path)
    
    # Veriyle birlikte HTML'yi doğrudan oluştur
    processed_html = generate_html_from_json(json_data, data)
    
    # BeautifulSoup ile parse et (pozisyon ayarlaması için)
    soup = BeautifulSoup(processed_html, "html.parser")
    
    # Tablo sonrası element konumlarını ayarla
    adjust_elements_after_table_processing(soup, json_data)
    
    # Güncellenmiş HTML'yi al
    final_html = str(soup)
    
    # Sonucu kaydet
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(final_html)
    
    print(f"JSON'dan HTML oluşturuldu ve işlendi: {output_path}")
    
    return final_html


def save_template_html(json_file_path, output_path):
    """JSON'dan sadece şablon HTML oluştur (veri işleme olmadan)"""
    # JSON'u yükle
    json_data = load_json_content(json_file_path)
    
    # Veri olmadan HTML şablonunu oluştur
    html_template = generate_html_template_only(json_data)
    
    # Sonucu kaydet
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_template)
    
    print(f"JSON'dan HTML şablonu oluşturuldu: {output_path}")
    
    return html_template
