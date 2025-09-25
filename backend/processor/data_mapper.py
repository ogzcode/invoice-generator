from currency_manager import CurrencyManager
from tax_manager import TaxManager
from utils import safe_get, format_date, format_discount, format_quantity_with_unit

class DataMapper:
    """Veri mapping işlemleri için sınıf"""
    
    def __init__(self):
        self.currency_manager = CurrencyManager()
        self.tax_manager = TaxManager()
        self._current_currency_id = 1
    
    def set_currency_id(self, currency_id):
        """Aktif para birimi ID'sini ayarla"""
        self._current_currency_id = currency_id
    
    def get_data_mapping(self):
        """Ana veri mapping'ini döndür"""
        return {
            # Müşteri bilgileri
            'name': lambda data: safe_get(data['customer'], 'name'),
            'address': lambda data: safe_get(data['customer'], 'address'),
            'phone': lambda data: safe_get(data['customer'], 'phone'),
            'taxOffice': lambda data: safe_get(data['customer'], 'taxOffice'),
            'taxNumber': lambda data: safe_get(data['customer'], 'vknTckn'),
            
            # Fatura bilgileri
            'dateOfIssue': lambda data: format_date(data['dateOfIssue']),
            'invoiceNo': lambda data: safe_get(data, 'invoiceNo'),
            'dispatchNo': lambda data: safe_get(data, 'dispatchNo'),
            'actualDispatchDate': lambda data: format_date(safe_get(data, 'actualDispatchDate')),
            'outgoingAddress': lambda data: safe_get(data, 'outgoingAddress'),
            'maturityDate': lambda data: format_date(data['maturityDate']),
            
            # Toplam alanları (para birimi ile)
            'subTotal': lambda data: self.currency_manager.format_currency_with_code(data['lineExtensionAmount'], data.get('currencyId', 1)),
            'totalAmount': lambda data: self.currency_manager.format_currency_with_code(data['payableAmount'], data.get('currencyId', 1)),
            'totalDiscount': lambda data: self.currency_manager.format_currency_with_code(data['allowanceTotalAmount'], data.get('currencyId', 1)),
            'totalStoppage': lambda data: self.currency_manager.format_currency_with_code(self.tax_manager.calculate_tax_total_by_type(data, 'is_stoppage'), data.get('currencyId', 1)),
            'totalAccommodationTax': lambda data: self.currency_manager.format_currency_with_code(self.tax_manager.calculate_tax_total_by_code(data, '0059'), data.get('currencyId', 1)),
            'totalVat': lambda data: self.currency_manager.format_currency_with_code(self.tax_manager.calculate_tax_total_by_code(data, '0015'), data.get('currencyId', 1)),
            'totalExciseDuty': lambda data: self.currency_manager.format_currency_with_code(self.tax_manager.calculate_excise_duty_total(data), data.get('currencyId', 1)),
            'totalCommunicationTax': lambda data: self.currency_manager.format_currency_with_code(self.tax_manager.calculate_tax_total_by_code(data, '4080'), data.get('currencyId', 1)),
            'totalWithholdingTax': lambda data: self.currency_manager.format_currency_with_code(self.tax_manager.calculate_withholding_tax_total(data), data.get('currencyId', 1)),
            'totalWithText': lambda data: self.currency_manager.number_to_text_turkish(data['payableAmount'], data.get('currencyId', 1)),
            
            # Özel notlar
            'orderDate': lambda data: format_date(safe_get(data, 'orderDate')),
            'orderInfo': lambda data: safe_get(data, 'orderInfo')
        }
    
    def get_product_mapping(self):
        """Ürün tablosu mapping'ini döndür"""
        return {
            'name': lambda item: safe_get(item['product'], 'name'),
            'description': lambda item: safe_get(item, 'description'),
            'code': lambda item: safe_get(item['product'], 'stockCode'),
            'quantity': lambda item: format_quantity_with_unit(item),
            'unitPrice': lambda item: self.currency_manager.format_currency_with_code(item['unitPrice'], self._current_currency_id),
            'discount': lambda item: format_discount(safe_get(item, 'discount')),
            'exciseDuty': lambda item: self.tax_manager.get_tax_percent_by_codes(item, ['0071', '9077', '0073', '0074', '0075', '0076', '0077']),
            'vatRate': lambda item: self.tax_manager.get_vat_rate_from_other_taxes(item),
            'communication': lambda item: self.tax_manager.get_tax_percent_by_codes(item, ['4080', '4081']),
            'accomodation': lambda item: self.tax_manager.get_tax_percent_by_codes(item, ['0059']),
            'withholdingTaxId': lambda item: self.tax_manager.format_withholding_tax_info_with_currency(item, self._current_currency_id),
            'total': lambda item: self.currency_manager.format_currency_with_code(item['total'], self._current_currency_id)
        }