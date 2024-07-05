from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r"books",BookViewSet,basename='book')



urlpatterns=[
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('books/', BookView.as_view(), name='book-list'),
    # path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path("",include(router.urls)),
]