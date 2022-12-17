from django.shortcuts import redirect
from .models import EmailVerification
from django.contrib import messages
from django.contrib.auth import logout
def MyMiddleware(get_response):
    print('initilazed middleware process')
    def myfunc(request):
        if request.user.is_authenticated:
            if not EmailVerification.objects.filter(user=request.user):
                email = EmailVerification(user=request.user)
                email.save()
            email = EmailVerification.objects.get(user=request.user)
            if not email.verify:
                messages.error(request,'Email not verified! First verify your email, kindly check your mail.')
                logout(request)
                return redirect('login')
        response = get_response(request)
        return response
    return myfunc
