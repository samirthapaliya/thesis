from django import template
from notification.models import Notification

register = template.Library()


@register.inclusion_tag('components/navbar_notification.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(
        to_user=request_user).exclude(has_seen=True).order_by('-datetime')
    return {'notifications': notifications, 'user': request_user}

@register.inclusion_tag('adminbusiness/base/notification.html', takes_context=True)
def Business_show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(
        to_user=request_user).exclude(has_seen=True).order_by('-datetime')
    limit_notifications = Notification.objects.filter(
        to_user=request_user).exclude(has_seen=True).order_by('-datetime')[:5]    
    return {'notifications': notifications, 'limit_notifications':limit_notifications, 'user': request_user}