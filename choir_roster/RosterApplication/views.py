from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ChoirMemberRegistrationForm, ChoirMemberProfileForm
from .models import ChoirMember, ChatMessage
from django.db import models
from django.contrib.auth import login
from django.conf import settings
import os
from django.http import JsonResponse
from django.db.models import Q

@login_required
def home(request):
    return render(request, 'RosterApplication/home.html')

def register(request):
    if request.method == 'POST':
        form = ChoirMemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('roster:home')
    else:
        form = ChoirMemberRegistrationForm()
    return render(request, 'RosterApplication/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'RosterApplication/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ChoirMemberProfileForm(request.POST, request.FILES, instance=request.user.choirmember)
        if form.is_valid():
            form.save()
            return redirect('roster:members')
    else:
        form = ChoirMemberProfileForm(instance=request.user.choirmember)
    
    return render(request, 'RosterApplication/profile_edit.html', {
        'form': form,
        'current_picture': request.user.choirmember.profile_picture
    })

def member_grid(request):
    members = ChoirMember.objects.filter(active=True).select_related('user')
    
    # Get unread message counts for each member
    unread_counts = {}
    if request.user.is_authenticated:
        for member in members:
            count = ChatMessage.objects.filter(
                sender=member,
                receiver=request.user.choirmember,
                is_read=False
            ).count()
            unread_counts[member.id] = count
    
    return render(request, 'roster/member_grid.html', {
        'members': members,
        'unread_counts': unread_counts
    })

@login_required
def chat_view(request, member_id):
    other_member = get_object_or_404(ChoirMember, id=member_id)
    current_member = request.user.choirmember
    
    # Mark messages as read
    ChatMessage.objects.filter(
        sender=other_member,
        receiver=current_member,
        is_read=False
    ).update(is_read=True)
    
    # Get chat history
    messages = ChatMessage.objects.filter(
        (models.Q(sender=current_member, receiver=other_member) |
         models.Q(sender=other_member, receiver=current_member))
    ).order_by('timestamp')
    
    return render(request, 'roster/chat.html', {
        'other_member': other_member,
        'messages': messages,
    })

def style_guide(request):
    pdf_path = os.path.join(settings.STATIC_ROOT, 'pdfs/style_guide.pdf')
    return render(request, 'RosterApplication/style_guide.html', {
        'pdf_url': settings.STATIC_URL + 'pdfs/style_guide.pdf'
    })

@login_required
def get_messages(request, member_id):
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user.choirmember, receiver_id=member_id) |
         Q(sender_id=member_id, receiver=request.user.choirmember))
    ).order_by('timestamp')
    return JsonResponse({'messages': list(messages.values())})

@login_required
def send_message(request, member_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        receiver = get_object_or_404(ChoirMember, id=member_id)
        
        ChatMessage.objects.create(
            sender=request.user.choirmember,
            receiver=receiver,
            message=message,
            is_read=False
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
