import json

class CurrencyManager:
    """Para birimi işlemleri için yönetici sınıf"""
    
    def __init__(self):
        self.currencies = self.load_currencies()
    
    def load_currencies(self):
        """Currencies.json dosyasını yükle"""
        try:
            with open('currencies.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            return []
    
    def get_currency_code(self, currency_id):
        """Currency ID'sine göre para birimi kodunu getir"""
        for currency in self.currencies:
            if currency['currencyId'] == currency_id:
                return currency['code']
        return 'TRY'  # Varsayılan
    
    def format_currency(self, amount):
        """Para formatını Türk lirası formatına çevir"""
        if amount is None or amount == 'None':
            return '0,00'
        try:
            return f"{float(amount):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return '0,00'
    
    def format_currency_with_code(self, amount, currency_id):
        """Para formatını para birimi kodu ile birlikte çevir"""
        formatted_amount = self.format_currency(amount)
        currency_code = self.get_currency_code(currency_id)
        return f"{formatted_amount} {currency_code}"
    
    def number_to_text_turkish(self, amount, currency_id=1):
        """Sayıyı Türkçe yazıya çevir"""
        if amount is None or amount == 'None':
            return 'sıfır lira'
        
        try:
            amount = float(amount)
            integer_part = int(amount)
            decimal_part = round((amount - integer_part) * 100)
            
            # Para birimi bilgisi
            currency_info = next((c for c in self.currencies if c['currencyId'] == currency_id), None)
            currency_name = 'lira' if not currency_info else currency_info['name'].lower()
            
            # Sayı isimleri
            ones = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
            tens = ['', '', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
            teens = ['on', 'onbir', 'oniki', 'onüç', 'ondört', 'onbeş', 'onaltı', 'onyedi', 'onsekiz', 'ondokuz']
            
            def convert_hundreds(num):
                if num == 0:
                    return ''
                elif num < 10:
                    return ones[num]
                elif num < 20:
                    return teens[num - 10]
                elif num < 100:
                    ten_digit = num // 10
                    one_digit = num % 10
                    return tens[ten_digit] + (ones[one_digit] if one_digit > 0 else '')
                else:
                    hundred_digit = num // 100
                    remainder = num % 100
                    hundred_text = 'yüz' if hundred_digit == 1 else ones[hundred_digit] + 'yüz'
                    return hundred_text + convert_hundreds(remainder)
            
            def convert_to_text(num):
                if num == 0:
                    return 'sıfır'
                elif num < 1000:
                    return convert_hundreds(num)
                elif num < 1000000:
                    thousands = num // 1000
                    remainder = num % 1000
                    thousand_text = 'bin' if thousands == 1 else convert_hundreds(thousands) + 'bin'
                    return thousand_text + convert_hundreds(remainder)
                elif num < 1000000000:
                    millions = num // 1000000
                    remainder = num % 1000000
                    million_text = 'birmilyon' if millions == 1 else convert_hundreds(millions) + 'milyon'
                    return million_text + convert_to_text(remainder)
                else:
                    return str(num)  # Çok büyük sayılar için
            
            result = convert_to_text(integer_part) + ' ' + currency_name
            
            if decimal_part > 0:
                if currency_id == 1:  # TRY için kuruş
                    result += ' ' + convert_to_text(decimal_part) + ' kuruş'
                else:  # Diğer para birimleri için cent
                    result += ' ' + convert_to_text(decimal_part) + ' cent'
            
            return result
            
        except:
            return 'sıfır ' + (currency_info['name'].lower() if currency_info else 'lira')