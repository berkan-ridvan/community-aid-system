from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ServiceRequest, Bid, User, Review, Message, Notification
from .forms import UserRegisterForm, ServiceRequestForm, BidForm, ReviewForm, MessageForm, ProfileForm
from django.http import Http404
from django.utils import timezone

def get_unread_notifications_count(user):
    return Notification.objects.filter(user=user, is_read=False).count()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'community/register.html', {'form': form})

@login_required
def home(request):
    unread_notifications_count = get_unread_notifications_count(request.user)
    if request.user.is_resident:
        service_requests = ServiceRequest.objects.filter(resident=request.user).order_by('-created_at')
        return render(request, 'community/home.html', {
            'service_requests': service_requests,
            'unread_notifications_count': unread_notifications_count
        })
    elif request.user.is_service_provider:
        available_requests = ServiceRequest.objects.filter(status='pending').order_by('-created_at')
        return render(request, 'community/home.html', {
            'available_requests': available_requests,
            'unread_notifications_count': unread_notifications_count
        })
    else:
        return render(request, 'community/home.html', {
            'unread_notifications_count': unread_notifications_count
        })

@login_required
def create_service_request(request):
    if not request.user.is_resident:
        messages.warning(request, 'You are not authorized to perform this action.')
        return redirect('home')
    
    unread_notifications_count = get_unread_notifications_count(request.user)
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.resident = request.user
            service_request.save()
            messages.success(request, 'Service request created successfully.')
            return redirect('home')
    else:
        form = ServiceRequestForm()
    return render(request, 'community/create_service_request.html', {
        'form': form,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    bids = Bid.objects.filter(service_request=service_request)
    unread_notifications_count = get_unread_notifications_count(request.user)
    
    if request.method == 'POST':
        if request.user.is_service_provider and service_request.status == 'pending':
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.save(commit=False)
                bid.service_request = service_request
                bid.service_provider = request.user
                bid.save()
                messages.success(request, 'Your bid has been sent successfully.')
                return redirect('service_request_detail', pk=pk)
        elif request.user.is_resident and service_request.status == 'completed':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.service_request = service_request
                review.reviewer = request.user
                review.reviewed = service_request.bids.filter(is_accepted=True).first().service_provider
                review.save()
                messages.success(request, 'Your review has been saved successfully.')
                return redirect('service_request_detail', pk=pk)
    else:
        if request.user.is_service_provider and service_request.status == 'pending':
            form = BidForm()
        elif request.user.is_resident and service_request.status == 'completed':
            form = ReviewForm()
        else:
            form = None
    
    return render(request, 'community/service_request_detail.html', {
        'service_request': service_request,
        'bids': bids,
        'form': form,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    if request.user != bid.service_request.resident:
        messages.warning(request, 'You are not authorized to perform this action.')
        return redirect('home')
    
    bid.is_accepted = True
    bid.save()
    bid.service_request.status = 'in_progress'
    bid.service_request.save()
    messages.success(request, 'Bid accepted.')
    return redirect('service_request_detail', pk=bid.service_request.pk)

@login_required
def complete_service(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.user != service_request.resident:
        messages.warning(request, 'You are not authorized to perform this action.')
        return redirect('home')
    
    service_request.status = 'completed'
    service_request.save()
    messages.success(request, 'Service request completed.')
    return redirect('home')

@login_required
def search_requests(request):
    query = request.GET.get('q', '')
    service_type = request.GET.get('service_type', '')
    urgency = request.GET.get('urgency', '')
    unread_notifications_count = get_unread_notifications_count(request.user)
    
    service_requests = ServiceRequest.objects.filter(status='pending')
    
    if query:
        service_requests = service_requests.filter(
            Q(description__icontains=query) |
            Q(resident__username__icontains=query)
        )
    
    if service_type:
        service_requests = service_requests.filter(service_type=service_type)
    
    if urgency:
        service_requests = service_requests.filter(urgency=urgency)
    
    return render(request, 'community/search_requests.html', {
        'service_requests': service_requests,
        'query': query,
        'service_type': service_type,
        'urgency': urgency,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def profile(request):
    unread_notifications_count = get_unread_notifications_count(request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            profile_picture_url = request.POST.get('profile_picture')
            if profile_picture_url:
                user.profile_picture = profile_picture_url
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'community/profile.html', {
        'form': form,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def messages_list(request, user_id=None):
    unread_notifications_count = get_unread_notifications_count(request.user)
    conversations = []
    users_with_messages = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()
    
    for other_user in users_with_messages:
        
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('-created_at').first()
        
        
        unread_count = Message.objects.filter(
            sender=other_user,
            receiver=request.user,
            is_read=False
        ).count()
        
        conversations.append({
            'other_user': other_user,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else timezone.now(), reverse=True)
    
    active_user = None
    messages = []
    if user_id:
        active_user = get_object_or_404(User, pk=user_id)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=active_user)) |
            (Q(sender=active_user) & Q(receiver=request.user))
        ).order_by('created_at')
        
        Message.objects.filter(
            sender=active_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
    
    return render(request, 'community/messages.html', {
        'conversations': conversations,
        'active_user': active_user,
        'active_user_id': user_id,
        'messages': messages,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('created_at')
    unread_notifications_count = get_unread_notifications_count(request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('chat', user_id=user_id)
    else:
        form = MessageForm()
    
    return render(request, 'community/chat.html', {
        'other_user': other_user,
        'messages': messages,
        'form': form,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    if request.method == 'POST':
        notifications.update(is_read=True)
        return redirect('notifications')
    
    return render(request, 'community/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'unread_notifications_count': unread_count
    })

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)
    unread_notifications_count = get_unread_notifications_count(request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')
    else:
        form = MessageForm()
    
    return render(request, 'community/send_message.html', {
        'form': form,
        'recipient': recipient,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    unread_notifications_count = get_unread_notifications_count(request.user)
    
    return render(request, 'community/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'unread_notifications_count': unread_notifications_count
    })

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    unread_notifications_count = get_unread_notifications_count(request.user)
    
    if message.sender != request.user and message.receiver != request.user:
        raise Http404
    
    if message.receiver == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'community/message_detail.html', {
        'message': message,
        'unread_notifications_count': unread_notifications_count
    })
