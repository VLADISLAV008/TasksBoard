from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'boards', views.BoardViewSet, basename='Boards')
router.register(r'user', views.UserViewSet)
router.register(r'user', views.UserDetailViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path(r'api-token-auth/', views.CustomAuthToken.as_view()),
]
