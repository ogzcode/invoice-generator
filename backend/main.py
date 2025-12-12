from html_process import process_html, load_file_content, save_html
from json_process import process_json_to_html

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

def test_html_processor():
    print("=== HTML Processor Test ===")
    
    # HTML şablonunu yükle
    html_template = load_file_content("./example.html")
    
    # HTML'yi işle
    processed_html = process_html(html_template, fake_date)
    
    # Sonucu dosyaya yaz
    save_html(processed_html, "./processed_invoice_html.html")
    
    print("HTML Processor tamamlandı!")


def test_json_processor():
    """JSON processor'u test et"""
    print("=== JSON Processor Test ===")
    
    # JSON'dan doğrudan veriyle HTML oluştur ve kaydet
    process_json_to_html("./test.json", fake_date, "./processed_invoice_json.html")
    
    print("JSON Processor tamamlandı!")


def main():
    print("Invoice Processor Test Suite")
    print("============================")
    
    test_json_processor()
    
    print("\nTüm işlemler tamamlandı!")


if __name__ == "__main__":
    main()
