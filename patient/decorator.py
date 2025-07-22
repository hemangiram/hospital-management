from functools import wraps
from django.shortcuts import redirect
from urllib.parse import quote

def allow_roles(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                print("User not authenticated. Redirecting to login...")
                return redirect(f'/login/?next={quote(request.path)}')

            print("Hello user")

            user_role = getattr(request.user.userprofile, 'role', None)
            if user_role:
                user_role = user_role.name.lower() 

            print(f"User role: {user_role}")

            if user_role in allowed_roles:
                print(f"Access granted for role: {user_role}")
                return view_func(request, *args, **kwargs)
            elif user_role == 'admin':  
                print(f"Access granted for admin role: {user_role}")
                return view_func(request, *args, **kwargs)
            else:
                print(f"Access denied for role: {user_role}")
                return redirect('home')  

        return wrapper
    return decorator
