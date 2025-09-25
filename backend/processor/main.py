import requests
import json
from invoice_processor import InvoiceProcessor, load_invoice_data, load_html_template, save_processed_html

invoice_request_url = "https://onmuhasebeapi.aysbulut.com/api/Invoice/getInvoiceById?id=1334"
template_request_url = "https://onmuhasebeapi.aysbulut.com/api/Template/getAllTemplate"
token = "eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJzZWxlY3RlZF9jb21wYW55X2lkIjoiMiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL2VtYWlsYWRkcmVzcyI6Im9ndXpoYW4uZ3VjQGF5c3NvZnQuY29tIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Ik_En3V6aGFuIiwiSWQiOiIyIiwibmJmIjoxNzU4NzAzMTU0LCJleHAiOjE3NTg3ODk1NTQsImlzcyI6ImF5c3NvZnRAYXlzc29mdC5jb20iLCJhdWQiOiJhc3lzb2Z0QGF5c3NvZnQuY29tIn0.s2rTGbNi3qI_aq0ennB4E2DUDZTHK9VbXszFoy-irk68rEFm4sGIXa6ybs7oM2e4SyD7Ui1ADF9n5qB5gh0nsw"

def get_template():
    # API isteği ile şablon verilerini al
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(template_request_url, headers=headers, json={"page": 1, "pageSize": 1000})


    if response.status_code == 200:
        data = response.json()
        return data["data"]["items"]
    else:
        print(f"Error: {response.status_code}")
        return None

def save_template_to_html(template, filename="output.html"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(template)

def get_invoice():
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(invoice_request_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data["data"])
        return data
    else:
        print(f"Error: {response.status_code}")
        return None
    
def save_invoice_data_to_file(invoice_data, filename="api_invoice.json"):
    """API'den gelen fatura verisini dosyaya kaydet"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(invoice_data, file, ensure_ascii=False, indent=2)

def process_invoice_with_template(template_html=None, invoice_data=None):
    """API verisini veya dosyadaki test verisini kullanarak HTML şablonunu doldur"""
    try:
        # Eğer veri verilmemişse dosyadan yükle
        if invoice_data is None:
            # Önce API'den kaydedilen dosyayı dene
            try:
                invoice_data = load_invoice_data('api_invoice.json')
                print("API'den kaydedilen fatura verisi yüklendi")
            except:
                # Yoksa test dosyasını kullan
                invoice_data = load_invoice_data('test.json')
                print("Test fatura verisi yüklendi")
        else:
            print("API'den gelen fatura verisi kullanılıyor")
        
        # HTML şablonunu yükle
        if template_html is None:
            # Önce API'den kaydedilen dosyayı dene
            try:
                html_template = load_html_template('api_template.html')
                print("API'den kaydedilen HTML şablonu yüklendi")
            except:
                # Yoksa mevcut dosyayı kullan
                html_template = load_html_template('Fatura Şablon 1.html')
                print("Mevcut HTML şablonu yüklendi")
        else:
            html_template = template_html
            print("API'den gelen HTML şablonu kullanılıyor")
        
        # Fatura işleyicisini oluştur
        processor = InvoiceProcessor()
        
        # HTML'i fatura verileriyle doldur
        processed_html = processor.process_invoice_html(html_template, invoice_data)
        print("HTML fatura verileriyle dolduruldu")
        
        # İşlenmiş HTML'i kaydet
        output_filename = 'processed_invoice.html'
        save_processed_html(processed_html, output_filename)
        print(f"İşlenmiş fatura {output_filename} olarak kaydedildi")
        
        return output_filename
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Fatura İşleme Sistemi Başlatılıyor...")
    
    # API'den şablon verilerini çek
    print("\n📋 Şablon verileri alınıyor...")
    template_data = get_template()
    
    if template_data:
        print(f"✅ {len(template_data)} şablon bulundu")
        
        # Kullanıcıdan şablon seçimi iste
        selected_id = input("\nLütfen bir şablon ID'si girin (veya Enter'a basarak varsayılan şablonu kullanın): ")
        
        selected_template_html = None
        if selected_id.strip():
            # API'den şablon seç
            selected_template = next((item for item in template_data if str(item["id"]) == selected_id), None)
            if selected_template:
                template_filename = selected_template["templateName"].replace(" ", "_") + ".html"
                save_template_to_html(selected_template["templateContent"], filename=template_filename)
                # API'den gelen şablonu dosyaya da kaydet (kolay erişim için)
                save_template_to_html(selected_template["templateContent"], filename="api_template.html")
                print(f"✅ Şablon {template_filename} ve api_template.html olarak kaydedildi")
                selected_template_html = selected_template["templateContent"]
            else:
                print("❌ Belirtilen ID'de şablon bulunamadı, varsayılan şablon kullanılacak")
        else:
            print("ℹ️ Varsayılan şablon kullanılacak")
    else:
        print("⚠️ Şablon verileri alınamadı, varsayılan şablon kullanılacak")
    
    # API'den fatura verisini çek
    print("\n💰 Fatura verisi alınıyor...")
    api_invoice_response = get_invoice()
    
    invoice_data_to_use = None
    if api_invoice_response:
        invoice_data_to_use = api_invoice_response["data"]
        # API verisini dosyaya kaydet
        save_invoice_data_to_file(invoice_data_to_use, "api_invoice.json")
        print("✅ Fatura verisi alındı ve api_invoice.json olarak kaydedildi")
    else:
        print("⚠️ API'den fatura verisi alınamadı, dosyadaki veriler kullanılacak")
    
    # Fatura işlemeyi başlat
    print("\n⚙️ Fatura işleniyor...")
    processed_file = process_invoice_with_template(selected_template_html, invoice_data_to_use)
    
    if processed_file:
        print(f"\n🎉 BAŞARILI! İşlenmiş fatura: {processed_file}")
        print("📁 Bu dosyayı web tarayıcınızda açarak sonucu görebilirsiniz.")
        print("\n📋 Kaydedilen dosyalar:")
        print("   📄 api_invoice.json - API'den gelen fatura verisi")
        if selected_template_html:
            print("   📄 api_template.html - API'den gelen şablon")
        print(f"   📄 {processed_file} - İşlenmiş fatura")
    else:
        print("\n❌ Fatura işleme başarısız oldu")
