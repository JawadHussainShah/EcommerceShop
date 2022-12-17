from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from requests import request
from .models import Product, Category, Orders, EmailVerification
from .forms import RegistrationForm, LoginForm, EditAminProfileForm, EditUserProfileForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .email_middleware import MyMiddleware

@MyMiddleware
def index(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    else:
        if request.POST.get('search'):
            search_item = request.POST.get('search')
            products = Product.objects.filter(name__contains=search_item)
            categories = Category.get_all_category()
            return render(request, 'store/index.html', {'products':products,
             'categories':categories})
        else:
            if request.method == 'POST':
                product = request.POST.get('product')
                remove = request.POST.get('remove')
                print(product)
                cart = request.session.get('cart')
                if cart:
                    quantity = cart.get(product)
                    if quantity:
                        if remove:
                            if quantity <= 1:
                                cart.pop(product)
                            else:
                                cart[product] = quantity - 1
                        else:
                            cart[product] = quantity + 1
                    else:
                        cart[product] = 1
                else:
                    cart = {}
                    cart[product] = 1
                request.session['cart'] = cart
                return redirect('home')
            cart = request.session.get('cart')
            if not cart:
                request.session.cart = {}
            id = request.GET.get('category')
            category = Category.objects.filter(id=id).first()
            if category:
                products = Product.objects.filter(category=category)
            else:
                products = Product.get_all_products()
        categories = Category.get_all_category()
        return render(request, 'store/index.html', {'products':products,
         'categories':categories})


def signup(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            messages.success(request, 'Account Created Successfully!')
            send_mail('Email VErification', 'Hi, ' + request.POST['username'] + ' Click the link below to verify your email...\n\nhttp://127.0.0.1:8000/email/' + request.POST['username'] + '/', 'Django@admin.com', [
             request.POST['email']])
    else:
        reg_form = RegistrationForm()
    return render(request, 'store/signup.html', {'form': reg_form})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            login_form = LoginForm(request=request, data=(request.POST))
            if login_form.is_valid():
                name = login_form.cleaned_data['username']
                upass = login_form.cleaned_data['password']
                user = authenticate(username=name, password=upass)
                if user:
                    login(request, user)
                    return redirect('home')
        else:
            login_form = LoginForm()
        return render(request, 'store/login.html', {'form': login_form})


def product_cart(request):
    cart_products=[]
    cart = request.session.get('cart')
    if not cart:
        request.session.cart = {}
    else:
        if cart:
            ids = list(request.session.get('cart').keys())
        else:
            ids = []
        cart_products = Product.objects.filter(id__in=ids)
    return render(request, 'store/cart.html', {'products': cart_products})


@login_required
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        user = request.user
        cart = request.session.get('cart')
        if cart:
            products = Product.objects.filter(id__in=(list(cart.keys())))
            for product in products:
                order = Orders(product=product, customer=user, quantity=(cart.get(str(product.id))), price=(product.price),
                  adress=address,
                  phone=phone)
                order.save()

            request.session['cart'] = {}
            messages.success(request, 'Check Out Successfully!')
        else:
            messages.warning(request, 'No Product Found in Cart!')
            return redirect('cart')
    return redirect('cart')


@login_required
def view_orders(request):
    order_list = Orders.objects.filter(customer=(request.user)).order_by('-date')
    return render(request, 'store/orders.html', {'orders': order_list})


def user_logout(request):
    logout(request)
    return redirect('home')


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser:
                fm = EditAminProfileForm((request.POST), instance=(request.user))
            else:
                fm = EditUserProfileForm((request.POST), instance=(request.user))
            if fm.is_valid():
                messages.success(request, 'Data changed successfully!')
                fm.save()
        else:
            if request.user.is_superuser:
                fm = EditAminProfileForm(instance=(request.user))
            else:
                fm = EditUserProfileForm(instance=(request.user))
        return render(request, 'store/profile.htm', {'name':request.user,  'form':fm})
    else:
        return HttpResponseRedirect('/login/')


def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=(request.user), data=(request.POST))
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Change password successflly!')
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=(request.user))
        return render(request, 'store/changepassword.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


def email_confirm(request, user):
    mail_state = ''
    invalid = ''
    print('------------------------->',request.method)
    # if request.method == 'POST':
        
    print('user---------------> ', user)
    check_user = User.objects.filter(username=user).first()
    if check_user:
        user_verify = EmailVerification(user=check_user, verify=True)
        user_verify.save()
        messages.success(request, 'Email Verified')
        mail_state = EmailVerification.objects.get(user=check_user)
    else:
        return redirect('/+lajfuewjncakmc8u43' + user + '@#$%#ka')
    return render(request, 'store/verifyemail.html', {'useremail':mail_state,  'invalid_link':invalid})