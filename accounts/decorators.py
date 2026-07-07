from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:

            if request.user.role == "admin":
                return view_func(request, *args, **kwargs)

        return redirect("account_login")

    return wrapper

# def member_required(view_func):
#     def wrapper(request, *args, **kwargs):

#         if request.user.is_authenticated:
#             # print('hello',request.user.role)
#             if request.user.role == "member":
#                 return view_func(request, *args, **kwargs)

#         return redirect("account_login")

#     return wrapper