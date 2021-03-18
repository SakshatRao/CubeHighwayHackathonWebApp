from django.contrib.auth.decorators import user_passes_test

# Checks whether current user is a customer
def is_customer(request):
    try:
        _ = request.user.customer
        return True
    except:
        return False

# Decorator function to check patient login
def customer_access():
    def check_customer(user):
        try:
            _ = user.customer
            return True
        except:
            return False
    return user_passes_test(check_customer, login_url = 'unauthorized')

# Decorator function to check admin login
def admin_access():
    def check_admin(user):
        if(user.is_superuser):
            return True
        else:
            return False
    return user_passes_test(check_admin, login_url='unauthorized')

# Returns patient access in a dictionary for passing to the HTTP files
# Other variables are also added to this function before being passed to the HTTP pages
def http_dict_func(request):
    return {'is_customer': is_customer(request)}