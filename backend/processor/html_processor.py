import re
from bs4 import BeautifulSoup

class HTMLProcessor:
    """HTML işleme ve düzenleme için sınıf"""
    
    def __init__(self, currency_manager, tax_manager):
        self.currency_manager = currency_manager
        self.tax_manager = tax_manager
    
    def calculate_table_height(self, invoice_items):
        """Tablo yüksekliğini hesapla"""
        # Her ürün satırı yaklaşık 35px
        base_header_height = 50
        row_height = 35
        total_height = base_header_height + (len(invoice_items) * row_height)
        return total_height

    def adjust_element_positions(self, soup, table_height):
        """Tablo altındaki elementlerin pozisyonlarını ayarla"""
        base_table_top = 150
        new_elements_top = base_table_top + table_height + 50  # 50px boşluk
        
        # Belirli bir düzende elementleri yerleştir
        # Sol taraf: totalWithText
        # Sağ taraf: subTotal, totalDiscount, totalVat, totalAmount (dikey sırada)
        
        # Sol taraf elementleri (yazı ile toplam)
        left_side_elements = ['totalWithText']
        
        # Sağ taraf elementleri (rakamsal toplamlar)
        right_side_elements = ['subTotal', 'totalDiscount', 'totalVat', 'totalAmount']
        
        # Sol taraf elementlerini yerleştir
        for data_key in left_side_elements:
            element = soup.find(attrs={'data-key': data_key})
            if element:
                style = element.get('style', '')
                # Sol tarafta ve tablo altında konumlandır
                style = re.sub(r'top:\s*\d+px', f'top: {new_elements_top}px', style)
                style = re.sub(r'left:\s*\d+px', 'left: 20px', style)  # Sol tarafa hizala
                element['style'] = style
        
        # Sağ taraf elementlerini dikey olarak yerleştir
        current_top = new_elements_top
        for data_key in right_side_elements:
            element = soup.find(attrs={'data-key': data_key})
            if element:
                style = element.get('style', '')
                # Sağ tarafta ve dikey sırayla konumlandır
                style = re.sub(r'top:\s*\d+px', f'top: {current_top}px', style)
                style = re.sub(r'left:\s*\d+px', 'left: 570px', style)  # Sağ tarafa hizala
                element['style'] = style
                current_top += 50  # Her element için 50px aralık
        
        # Diğer elementleri de kontrol et ve gerekirse yerleştir
        other_elements = [
            'totalStoppage', 'totalAccommodationTax', 'totalExciseDuty', 
            'totalCommunicationTax', 'totalWithholdingTax'
        ]
        
        for data_key in other_elements:
            element = soup.find(attrs={'data-key': data_key})
            if element:
                style = element.get('style', '')
                # Bu elementler varsa sağ tarafa yerleştir
                style = re.sub(r'top:\s*\d+px', f'top: {current_top}px', style)
                style = re.sub(r'left:\s*\d+px', 'left: 570px', style)
                element['style'] = style
                current_top += 50
    
    def create_product_row(self, item, soup, product_mapping):
        """Ürün satırı oluştur"""
        tr = soup.new_tag('tr')
        
        # HTML'deki mevcut thead'den sütun sayısı ve data-key'leri al
        table = soup.find('table')
        table_headers = []
        if table:
            thead = table.find('thead')
            if thead:
                header_row = thead.find('tr')
                if header_row:
                    header_cells = header_row.find_all('th')
                    # Tüm başlıklar için data-key veya pozisyon tabanlı mapping oluştur
                    for i, cell in enumerate(header_cells):
                        data_key = cell.get('data-key')
                        if data_key:
                            table_headers.append(data_key)
                        else:
                            # data-key yoksa pozisyona göre mapping yap
                            # Bu örnekte 7 sütun var: name, quantity, unitPrice, vatRate(indirim), KDV, Kdv Tevkifatı, Ürün Toplamı
                            position_mapping = {
                                4: 'vatRate',  # KDV sütunu (vatRate olarak mapping)
                                5: 'withholdingTaxId',  # Kdv Tevkifatı sütunu  
                                6: 'total'   # Ürün Toplamı sütunu
                            }
                            if i in position_mapping:
                                table_headers.append(position_mapping[i])
                            else:
                                table_headers.append(f'column_{i}')  # Fallback
        
        # Eğer header bulunamazsa varsayılan sırayı kullan
        if not table_headers:
            table_headers = ['name', 'quantity', 'unitPrice', 'vatRate', 'vatRate', 'withholdingTaxId', 'total']
        
        for header_key in table_headers:
            td = soup.new_tag('td')
            td['style'] = 'border: 1px solid #d1d5db; padding: 8px 16px; color: #374151;'
            
            if header_key in product_mapping:
                try:
                    value = product_mapping[header_key](item)
                    td.string = value
                except Exception as e:
                    print(f"Error processing {header_key}: {e}")
                    td.string = ''
            else:
                # Bilinmeyen sütunlar için boş değer
                td.string = ''
            
            # Hizalama ayarları
            if header_key in ['quantity', 'discount']:
                td['style'] += ' text-align: left;'
            elif header_key == 'total':
                td['style'] += ' text-align: right;'
                
            tr.append(td)
        
        return tr

    def process_invoice_html(self, html_content, invoice_data, data_mapping, product_mapping):
        """Fatura HTML'ini işle ve verilerle doldur"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Ana data-key alanlarını doldur
        for data_key, mapping_func in data_mapping.items():
            element = soup.find(attrs={'data-key': data_key})
            if element:
                try:
                    value = mapping_func(invoice_data)
                    # Mevcut metni değiştir
                    if element.string:
                        current_text = element.string
                        if ':' in current_text:
                            label = current_text.split(':')[0] + ':'
                            element.string = f"{label} {value}"
                        else:
                            element.string = value
                    else:
                        element.string = value
                    
                    # Width ayarlamalarını yap (tablo dışındaki alanlar için)
                    if data_key not in ['undefined']:  # Tablo alanını hariç tut
                        style = element.get('style', '')
                        if 'width:' in style:
                            style = re.sub(r'width:\s*\d+px', 'width: 400px', style)
                        else:
                            style += '; width: 400px'
                        element['style'] = style
                        
                except Exception as e:
                    print(f"Error processing {data_key}: {e}")

        # Tabloyu işle
        table = soup.find('table')
        if table:
            tbody = table.find('tbody')
            if tbody:
                # Mevcut tbody içeriğini temizle
                tbody.clear()
                
                # Ürün satırlarını ekle
                for item in invoice_data.get('invoiceItems', []):
                    product_row = self.create_product_row(item, soup, product_mapping)
                    tbody.append(product_row)
                
                # Tablo yüksekliğini hesapla ve pozisyonları ayarla
                table_height = self.calculate_table_height(invoice_data.get('invoiceItems', []))
                self.adjust_element_positions(soup, table_height)

        return str(soup)