from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

# Initialize DefaultRouter
router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

# Create nested router for messages
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]