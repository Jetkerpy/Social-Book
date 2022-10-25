from django.urls import path
from .views import (
    send_message_view,
    get_message_from_js,

)


app_name = 'chat'

urlpatterns = [
    path('', send_message_view, name = 'chat'),
    path('message/', get_message_from_js, name = 'message'),





]