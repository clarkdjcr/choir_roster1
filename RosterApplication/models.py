from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class ChoirMember(models.Model):
    VOICE_PARTS = [
        ('S1', 'Soprano 1'),
        ('S2', 'Soprano 2'),
        ('A1', 'Alto 1'),
        ('A2', 'Alto 2'),
        ('T1', 'Tenor 1'),
        ('T2', 'Tenor 2'),
        ('B1', 'Bass 1'),
        ('B2', 'Bass 2'),
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    voice_part = models.CharField(max_length=2, choices=VOICE_PARTS, null=True, blank=True)
    folder_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        unique=True,
        null=True,
        blank=True
    )
    phone_number = models.CharField(max_length=15, blank=True, default='')
    active = models.BooleanField(default=True)
    join_date = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'RosterApplication_choirmember'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_voice_part_display()}"

    def update_online_status(self, status):
        self.is_online = status
        self.save(update_fields=['is_online', 'last_seen'])

class Attendance(models.Model):
    member = models.ForeignKey(ChoirMember, on_delete=models.CASCADE)
    date = models.DateField()
    will_attend = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.member.user.username} - {self.date}"
    
class Performance(models.Model):
    date = models.DateField()
    song_title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.song_title} - {self.date}"

class ChatMessage(models.Model):
    sender = models.ForeignKey(ChoirMember, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(ChoirMember, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'From {self.sender} to {self.receiver} at {self.timestamp}'

class UnreadMessage(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    recipient = models.ForeignKey(ChoirMember, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']