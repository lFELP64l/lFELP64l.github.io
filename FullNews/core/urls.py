from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name="index"),
    path('adminfull/', adminfull, name="adminfull"),
    path('adminAgregar/', adminAgregar, name="adminAgregar"),
    path('adminEliminar/<id>', adminEliminar, name="adminEliminar"),
    path('login/', email_login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('indexPeriodista/', indexPeriodista, name='indexPeriodista'),
    path('adminPeriodistas/', adminPeriodistas, name='adminPeriodistas'),
    path('crear_noticia/', crear_noticia, name='crear_noticia'),
    path('cambiar_estado/<int:new_id>/', cambiar_estado, name='cambiar_estado'),
    path('mis_noticias/', mis_noticias, name='mis_noticias'),
    path('categorias/<int:categoria_id>/', filtrar_news_por_categoria, name='filtrar_news_por_categoria'),
    path('filtroUsuario/', filtroUsuario, name='filtroUsuario'),
    path('noticia/<int:new_id>/', detalle_noticia, name='detalle_noticia'),
    path('bloqueado', lock_account, name='bloqueado'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/contrasena_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/contrasena_reset_enviado.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/contrasena_reset_hecho.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/contrasena_reset_completo.html'), name='password_reset_complete'),
    
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('salir_to_cart/<int:product_id>/', salir_to_cart, name='salir_to_cart'),
    path('cart/', cart, name='cart'),
]
