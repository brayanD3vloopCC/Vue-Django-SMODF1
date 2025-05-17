from django.urls import path
from .views import RegistroView, LoginView, LogoutView, UsuarioActualView, PerfilUpdateView

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usuario-actual/', UsuarioActualView.as_view(), name='usuario-actual'),
    path('me/', UsuarioActualView.as_view(), name='usuario-actual-me'),
    path('perfil/', PerfilUpdateView.as_view(), name='perfil-update'),
] 