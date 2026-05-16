from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, default='New conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.username} — {self.title}'


class Message(models.Model):
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLE_SYSTEM = 'system'
    ROLE_CHOICES = [(ROLE_USER, 'User'), (ROLE_ASSISTANT, 'Assistant'), (ROLE_SYSTEM, 'System')]

    AGENT_CLAUDE = 'claude'
    AGENT_ANNOTATION = 'annotation'
    AGENT_CUSTOM = 'custom'
    AGENT_CHOICES = [(AGENT_CLAUDE, 'Claude'), (AGENT_ANNOTATION, 'Annotation'), (AGENT_CUSTOM, 'Custom')]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    agent = models.CharField(max_length=20, choices=AGENT_CHOICES, default=AGENT_CLAUDE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'agent': self.agent,
            'content': self.content,
            'created_at': self.created_at.strftime('%H:%M'),
        }
