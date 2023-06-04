from django.template.defaulttags import register

@register.simple_tag   
def get_item(dictionary, groupname, weekday, lesson, key):                   
    try:
        return dictionary[groupname][int(weekday)][lesson][key][:10]
    except:            
        return "-"

@register.simple_tag   
def get_item2(dictionary, groupname, weekday, lesson, key):                   
    try:
        return dictionary[groupname][int(weekday)][int(lesson)][key][:10]
    except:            
        return "-"