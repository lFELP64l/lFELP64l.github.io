from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.exceptions import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.db.models import Count
from django.core.paginator import Paginator
from django.conf import settings
import requests
import paypalrestsdk

# Create your views here.
def index (request):
    categorias = CateNew.objects.all()
    aux = {
        'lista' : categorias
    }
    
    return render(request, 'core/index.html', aux)

@login_required
def detalle_noticia(request, new_id):
    new = get_object_or_404(New, pk=new_id)
    return render(request, 'core/detalle_noticia.html', {'new': new})

@login_required
def filtroUsuario(request):
    if request.method == 'POST':
        form = UserFilterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(first_name=username)
                filtered_news = New.objects.filter(autor=user)
            except User.DoesNotExist:
                filtered_news = []
            return render(request, 'core/usuarioFiltrado.html', {'news': filtered_news, 'username': username, 'form': form})
    else:
        form = UserFilterForm()
    return render(request, 'core/filtroUsuario.html', {'form': form})

@login_required
def adminfull (request):
    news = New.objects.filter(estadoNew=1)
    
    aux = {
        'lista': news
    }
            
    return render(request, 'core/adminfull/adminfull.html', aux)

@login_required
def filtrar_news_por_categoria(request, categoria_id):
    categoria = get_object_or_404(CateNew, pk=categoria_id)
    news_filtradas = New.objects.filter(categoria=categoria)
    
    paginator = Paginator(news_filtradas, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categorias = CateNew.objects.all()

    return render(request, 'core/filtered_news_list.html', {'page_obj': page_obj, 'categoria': categoria})

@login_required
def adminAgregar (request):
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Periodista creado correctamente')
            return redirect('/adminAgregar/')
        else:
            messages.error(request, 'Error al guardar')
    else:
        form = StaffUserCreationForm()
             
    return render(request, 'core/adminfull/adminAgregar.html', {'form': form})

@login_required
def adminPeriodistas (request):
    periodistas = User.objects.filter(is_superuser=False).annotate(news_count=Count('new'))
    
    aux = {
        'lista': periodistas
    }
    
    return render(request, 'core/adminfull/adminPeriodistas.html', aux)

@login_required
def adminEliminar (request, id):
    user = User.objects.get(id=id)
    user.delete()
     
    return redirect(to="adminPeriodistas")

User = get_user_model()

def email_login_view(request):
    logout(request)
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email__iexact=email)
                user = authenticate(request, email=user.email, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('/adminfull/')
                    elif user.is_staff:
                        return redirect('/indexPeriodista/')
                    else:
                        return redirect('/')
                else:
                    messages.error(request, 'Email o contraseña incorrectos')
            except User.DoesNotExist:
                messages.error(request, 'Email o contraseña incorrectos')
    else:
        form = EmailLoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    logout(request)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente')
            return redirect('login')
        else:
            messages.error(request, 'Error al guardar')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def indexPeriodista(request):
    return render(request, 'core/periodista/indexPeriodista.html')

@login_required
def crear_noticia(request):
    if request.method == 'POST':
        form = NewForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.autor = request.user
            
            # Obtener la ubicación utilizando la API de Nominatim
            location = request.POST.get('location')
            if location:
                response = requests.get('https://nominatim.openstreetmap.org/search', 
                                        params={'q': location, 'format': 'json'})
                if response.status_code == 200 and response.json():
                    location_details = response.json()[0]['display_name']
                    new.ubicacion = location_details
                else:
                    messages.error(request, 'Ubicación no encontrada')
                    return render(request, 'core/periodista/crear_noticia.html', {'form': form})
            
            new.save()
            messages.success(request, 'Noticia creada satisfactoriamente')
            return redirect('crear_noticia')
        else:
            messages.error(request, 'Error al guardar')
    else:
        form = NewForm()
    return render(request, 'core/periodista/crear_noticia.html', {'form': form})

@login_required
def cambiar_estado(request, new_id):
    new = get_object_or_404(New, pk=new_id)
    if request.method == 'POST':
        estado_id = int(request.POST.get('estado'))
        if estado_id == 3:
            mensaje = request.POST.get('mensaje', '').strip()
            if not mensaje:
                return render(request, 'news_list.html', {
                    'news': New.objects.all(),
                    'error': 'Debe proporcionar un mensaje para cambiar el estado a 3.',
                })
            new.mensaje = mensaje
        new.estadoNew_id = estado_id
        new.save()
    return redirect('adminfull')

@login_required
def mis_noticias(request):
    user = request.user
    user_news = New.objects.filter(autor=user, estadoNew__in=[1, 3])
    
    aux = {
        'lista': user_news
    }
    
    return render(request, 'core/periodista/mis_noticias.html', aux)

def lock_account (request):
    logout(request)
    return render(request, 'core/lock_account.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Producto, id=product_id)
    cart_item, created = carritoItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def salir_to_cart(request, product_id):
    product = get_object_or_404(Producto, id=product_id)
    cart_item, created = carritoItem.objects.get_or_create(user=request.user, product=product)
    if cart_item.quantity > 1:
        if not created:
            cart_item.quantity = cart_item.quantity - 1
        cart_item.save()
    else:
        cart_item.quantity = 1
    return redirect('cart')

@login_required
def cart(request):
    cart_items = carritoItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



