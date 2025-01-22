from django.shortcuts import redirect
from django.urls import reverse

class AdminRedirectMiddleware:
    """
    Middleware to redirect non-admin users to the Django admin login panel when accessing restricted views.
    After authentication, redirects them to `/list_schedules/`.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Restricted path for the schedules list
        restricted_path = reverse('list_schedules')  # e.g., /list_schedules/
        admin_path = reverse('admin:index')  # e.g., /admin/

        # Avoid loops by checking if the user is already on the admin page or authenticated
        if request.path == restricted_path:
            if not request.user.is_authenticated or not request.user.is_staff:
                # Redirect non-authenticated or non-staff users to the admin login
                if request.path != admin_path:  # Prevent looping to admin
                    request.session['next'] = restricted_path
                    return redirect(admin_path)
            else:
                # If authenticated and staff, ensure they go to the restricted path
                next_url = request.session.pop('next', restricted_path)
                if request.path != next_url:
                    return redirect(next_url)

        return None
