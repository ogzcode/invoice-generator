import json
from currency_manager import CurrencyManager
from tax_manager import TaxManager
from html_processor import HTMLProcessor
from data_mapper import DataMapper

class InvoiceProcessor:
    """Ana fatura işleme sınıfı - diğer sınıfları koordine eder"""
    
    def __init__(self):
        # Yönetici sınıfları oluştur
        self.currency_manager = CurrencyManager()
        self.tax_manager = TaxManager()
        self.html_processor = HTMLProcessor(self.currency_manager, self.tax_manager)
        self.data_mapper = DataMapper()

    def process_invoice_html(self, html_content, invoice_data):
        """Fatura HTML'ini işle ve verilerle doldur"""
        # Currency ID'yi data mapper'a aktar
        currency_id = invoice_data.get('currencyId', 1)
        self.data_mapper.set_currency_id(currency_id)
        
        # Data mapping'leri al
        data_mapping = self.data_mapper.get_data_mapping()
        product_mapping = self.data_mapper.get_product_mapping()
        
        # HTML işlemeyi html_processor'a devret
        return self.html_processor.process_invoice_html(
            html_content, 
            invoice_data, 
            data_mapping, 
            product_mapping
        )

def load_invoice_data(filename):
    """Fatura verisini JSON dosyasından yükle"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_html_template(filename):
    """HTML şablonunu yükle"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def save_processed_html(content, filename):
    """İşlenmiş HTML'i kaydet"""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)