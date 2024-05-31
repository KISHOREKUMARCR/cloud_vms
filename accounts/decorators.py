from django.shortcuts import redirect

def login_required(function):
    def wrap(request, *args, **kwargs):
        
        if 'user_id' in request.session:
            current_user = request.session['user_id']
            print("\n decorater user_id : ",current_user)
            return function(request, *args, **kwargs)
        else:
            return redirect('loginprocess')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
    



def super_admin_only(function):
    def wrapper_func(request, *args, **kwargs):
        if 'user' in request.session:
            if 'roles' in request.session:
                role_name = request.session['roles']
                if role_name == "auth_admin":
                    return redirect('auth_admin')
                if role_name == "auth_user":
                    return redirect('vms_page')
                if role_name == "super_admin":
                    return function(request, *args, **kwargs)
    return wrapper_func            