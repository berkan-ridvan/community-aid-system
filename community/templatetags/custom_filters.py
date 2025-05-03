from django import template

register = template.Library()

@register.filter
def status_color(status):
    colors = {
        'pending': 'warning',
        'in_progress': 'info',
        'completed': 'success',
        'cancelled': 'danger',
    }
    return colors.get(status, 'secondary')

@register.filter
def urgency_color(urgency):
    colors = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger',
    }
    return colors.get(urgency, 'secondary') 