from django.urls import path
from . import views

app_name = "aiapp"
urlpatterns = [
    path("ask-ai/", views.ask_ai, name="ask_ai"),
    path("new/", views.new_chat, name="new_chat"),
    path("chat/<int:conversation_id>/", views.ask_ai, name="ask_ai_specific"),
]
