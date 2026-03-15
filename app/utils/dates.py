from datetime import datetime


def format_dt(value):
    if not value:
        return ''
    if isinstance(value, str):
        return value
    return value.strftime('%d/%m/%Y %H:%M')
