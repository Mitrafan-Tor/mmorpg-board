from django.urls import path
from .views import home, delete_advertisement
from .views import (
    create_advertisement, edit_advertisement, advertisement_detail,
    my_responses, accept_response, delete_response
)

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_advertisement, name='create_advertisement'),
    path('delete/<int:pk>/', delete_advertisement, name='delete_advertisement'),
    path('edit/<int:pk>/', edit_advertisement, name='edit_advertisement'),
    path('<int:pk>/', advertisement_detail, name='advertisement_detail'),
    path('responses/', my_responses, name='my_responses'),
    path('responses/accept/<int:pk>/', accept_response, name='accept_response'),
    path('responses/delete/<int:pk>/', delete_response, name='delete_response'),
]