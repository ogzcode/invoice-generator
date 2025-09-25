import json

class TaxManager:
    """Vergi hesaplamaları için yönetici sınıf"""
    
    def __init__(self):
        self.taxes = self.load_taxes()
    
    def load_taxes(self):
        """Taxes.json dosyasını yükle"""
        try:
            with open('taxes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get('data', [])
        except:
            return []
    
    def get_tax_percent_by_codes(self, item, tax_codes):
        """Belirli vergi kodlarına göre percent değerini al (ÖTV, İletişim Vergisi, Konaklama Vergisi için)"""
        other_taxes = item.get('otherTaxes', [])
        for tax in other_taxes:
            tax_code = tax.get('taxCategoryTypeCode')
            if tax_code in tax_codes:
                percent = tax.get('percent', 0)
                return f"%{percent}" if percent else '%0'
        return '%0'

    def get_vat_rate_from_other_taxes(self, item):
        """KDV oranını otherTaxes'in birinci elemanından al"""
        other_taxes = item.get('otherTaxes', [])
        if other_taxes and len(other_taxes) > 0:
            # İlk elemanı al (genellikle KDV)
            first_tax = other_taxes[0]
            percent = first_tax.get('percent', 0)
            return f"%{percent}" if percent else '%0'
        return '%0'
    
    def calculate_tax_total_by_code(self, invoice_data, tax_code):
        """Belirli vergi koduna göre toplam vergi tutarını hesapla"""
        total = 0
        for item in invoice_data.get('invoiceItems', []):
            for tax in item.get('otherTaxes', []):
                if tax.get('taxCategoryTypeCode') == tax_code:
                    total += float(tax.get('taxAmount', 0))
        return total

    def calculate_tax_total_by_type(self, invoice_data, tax_type):
        """Vergi tipine göre (is_stoppage, is_withholding) toplam vergi tutarını hesapla"""
        total = 0
        for item in invoice_data.get('invoiceItems', []):
            for tax in item.get('otherTaxes', []):
                tax_code = tax.get('taxCategoryTypeCode')
                # taxes.json'dan ilgili vergi tipini bul
                tax_info = next((t for t in self.taxes if t['code'] == tax_code), None)
                if tax_info and tax_info.get(tax_type):
                    total += float(tax.get('taxAmount', 0))
        return total

    def calculate_excise_duty_total(self, invoice_data):
        """ÖTV (Özel Tüketim Vergisi) toplam tutarını hesapla"""
        total = 0
        otv_codes = ['0071', '9077', '0073', '0074', '0075', '0076', '0077']  # ÖTV kodları
        for item in invoice_data.get('invoiceItems', []):
            for tax in item.get('otherTaxes', []):
                if tax.get('taxCategoryTypeCode') in otv_codes:
                    total += float(tax.get('taxAmount', 0))
        return total

    def calculate_withholding_tax_total(self, invoice_data):
        """Tevkifat vergisi toplam tutarını ürünlerin withholdingTax alanlarından hesapla"""
        total = 0
        for item in invoice_data.get('invoiceItems', []):
            withholding_tax = item.get('withholdingTax')
            if withholding_tax and withholding_tax.get('taxAmount'):
                total += float(withholding_tax.get('taxAmount', 0))
        return total
    
    def format_withholding_tax_info(self, item):
        """Tevkifat bilgilerini formatla (taxTypeCode, ratio, taxAmount)"""
        withholding_tax = item.get('withholdingTax')
        if not withholding_tax:
            return ''
        
        try:
            from utils import safe_get
            name = safe_get(withholding_tax, 'taxTypeCode', '')
            ratio = safe_get(withholding_tax, 'ratio', '')
            tax_amount = withholding_tax.get('taxAmount', 0)
            
            from currency_manager import CurrencyManager
            currency_manager = CurrencyManager()
            formatted_amount = currency_manager.format_currency(tax_amount)

            return f"{name}({ratio}) - {formatted_amount}" if formatted_amount and formatted_amount != '0,00' else name
        except:
            return ''

    def format_withholding_tax_info_with_currency(self, item, currency_id=1):
        """Tevkifat bilgilerini para birimi kodlu formatla (taxTypeCode, ratio, taxAmount)"""
        withholding_tax = item.get('withholdingTax')
        if not withholding_tax:
            return ''
        
        try:
            from utils import safe_get
            from currency_manager import CurrencyManager
            
            name = safe_get(withholding_tax, 'taxTypeCode', '')
            ratio = safe_get(withholding_tax, 'ratio', '')
            tax_amount = withholding_tax.get('taxAmount', 0)
            
            currency_manager = CurrencyManager()
            formatted_amount = currency_manager.format_currency_with_code(tax_amount, currency_id)

            return f"{name}({ratio}) - {formatted_amount}" if formatted_amount and formatted_amount != '0,00 TRY' else name
        except:
            return ''