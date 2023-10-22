from datetime import datetime

def datetimeformat(value, format='%d/%m/%Y %H:%M'):
    return value.strftime(format)
