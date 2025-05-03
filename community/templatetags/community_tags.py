from django import template

register = template.Library()

@register.filter
def status_color(status):
    if status == 'pending':
        return 'warning'
    elif status == 'in_progress':
        return 'info'
    elif status == 'completed':
        return 'success'
    elif status == 'cancelled':
        return 'danger'
    else:
        return 'secondary'

@register.filter(name='urgency_color')
def urgency_color(value):
    color_map = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger'
    }
    return color_map.get(value, 'secondary') 