from datetime import datetime

def safe_get(data, key, default=''):
    """Null, None, undefined değerler için güvenli değer alma"""
    if data is None:
        return default
    
    value = data.get(key, default) if isinstance(data, dict) else default
    
    # Null, None, undefined kontrolü
    if value is None or value == 'None' or value == 'null' or value == 'undefined':
        return default
        
    return value

def format_date(date_str):
    """Tarihi Türkçe formatına çevir"""
    if date_str and date_str != 'None':
        try:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00').split('T')[0])
            return date_obj.strftime('%d.%m.%Y')
        except:
            return ''
    return ''

def format_discount(discount):
    """İndirim formatını düzenle"""
    if discount is None or discount == 'None':
        return '%0'
    try:
        return f"%{float(discount)}"
    except:
        return '%0'

def format_quantity_with_unit(item):
    """Miktar + birim formatı"""
    quantity = str(item['quantity'])
    unit_name = ''
    
    # UnitType kontrolü
    if 'unitType' in item and item['unitType']:
        unit_name = safe_get(item['unitType'], 'name')
    
    if unit_name:
        return f"{quantity} {unit_name}"
    return quantity