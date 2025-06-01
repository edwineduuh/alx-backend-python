from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['participants']
    search_fields = ['participants__email', 'participants__first_name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        """Return only conversations involving the current user"""
        return self.request.user.conversations.all()

    def perform_create(self, serializer):
        """Create a new conversation with current user as participant"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to an existing conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = get_object_or_404(User, pk=user_id)
        conversation.participants.add(user)
        return Response(
            {'status': 'participant added'},
            status=status.HTTP_200_OK
        )

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conversation', 'sender', 'read']
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """Return only messages in conversations the user is part of"""
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        """Create a new message in a conversation"""
        conversation_id = self.request.data.get('conversation')
        conversation = get_object_or_404(
            Conversation,
            pk=conversation_id,
            participants=self.request.user
        )
        serializer.save(sender=self.request.user, conversation=conversation)