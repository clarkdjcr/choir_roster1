from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChoirMember, ChatMessage
from .forms import ProfileEditForm, ChoirMemberRegistrationForm
from django.contrib.auth import login, logout

@login_required
def get_messages(request, member_id):
    messages = ChatMessage.objects.filter(
        Q(sender=request.user.choirmember, receiver_id=member_id) |
        Q(sender_id=member_id, receiver=request.user.choirmember)
    ).order_by('timestamp')
    
    return JsonResponse({
        'messages': [{
            'message': msg.message,
            'sender_id': msg.sender.id,
            'timestamp': msg.timestamp.isoformat(),
            'is_read': msg.is_read
        } for msg in messages]
    })

@login_required
def send_message(request, member_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        receiver = get_object_or_404(ChoirMember, id=member_id)
        
        msg = ChatMessage.objects.create(
            sender=request.user.choirmember,
            receiver=receiver,
            message=message,
            is_read=False
        )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def member_grid(request):
    # Create ChoirMember if it doesn't exist
    if not hasattr(request.user, 'choirmember'):
        ChoirMember.objects.create(user=request.user)
    
    members = ChoirMember.objects.filter(active=True).select_related('user')
    return render(request, 'roster/member_grid.html', {
        'members': members
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.choirmember)
        if form.is_valid():
            form.save()
            return redirect('roster:members')
    else:
        form = ProfileEditForm(instance=request.user.choirmember)
    
    return render(request, 'RosterApplication/profile_edit.html', {
        'form': form
    })

@login_required
def home(request):
    return render(request, 'RosterApplication/home.html')

def register(request):
    if request.method == 'POST':
        form = ChoirMemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('roster:home')
    else:
        form = ChoirMemberRegistrationForm()
    return render(request, 'RosterApplication/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def chat_view(request, member_id):
    other_member = get_object_or_404(ChoirMember, id=member_id)
    return render(request, 'roster/chat.html', {
        'other_member': other_member
    }) 