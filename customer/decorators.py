from django.shortcuts import redirect


def customer_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('my-admin-dashboard')
        elif request.user.is_business:
            return redirect('businessDash')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function
