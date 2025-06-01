from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    bio = models.TextField(_('bio'), blank=True, null=True)
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    last_online = models.DateTimeField(_('last online'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Conversation(models.Model):
    """Model representing a conversation between users"""
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        verbose_name=_('participants')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('conversation')
        verbose_name_plural = _('conversations')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    """Model representing a message in a conversation"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('conversation')
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('sender')
    )
    content = models.TextField(_('content'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    read = models.BooleanField(_('read'), default=False)
    
    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

# Create your models here.
