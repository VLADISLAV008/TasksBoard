from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards import views

router = DefaultRouter()
router.register(r'boards', views.BoardViewSet, basename='board')
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'cards', views.CardViewSet, basename='card')
router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path(r'api-token-auth/', views.CustomAuthToken.as_view()),
]
