from django.template.defaulttags import register
    
@register.filter
def divide2(value, arg):
    try:        
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return None