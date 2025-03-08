
from django.shortcuts import redirect
from django.http import HttpResponse

def is_user_authenticated(view_func):
    def wrapper(request , *args , **kwargs):
       
        if request.user.is_authenticated:
            return redirect("homepage")
        else: 
            return view_func(request,*args,**kwargs)
        
    return wrapper


def allowed_pages(*allowed):
    def function(view_func):
        def wrapper(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                 
            if group in allowed:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("you cannot view this page")
        return wrapper
    return function

def admin_or_worker(view_func):
    def wrapper(request,*args,**kwargs):
        group = None
        
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
                
        if group == "admin":
            return redirect("adminpage")
        elif group == "worker":
            return view_func(request,*args,**kwargs)
        else: 
            return view_func(request,*args,**kwargs)
    return wrapper
        