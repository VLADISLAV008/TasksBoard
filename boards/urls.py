from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'boards', views.BoardViewSet, basename='Board')
router.register(r'sections', views.SectionViewSet, basename='Section')
router.register(r'cards', views.CardViewSet, basename='Card')
router.register(r'user', views.UserViewSet, basename='User')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path(r'api-token-auth/', views.CustomAuthToken.as_view()),
]
