from django.contrib import admin

class StrepAAdminSite(admin.AdminSite):
    site_header = 'Strep A Database'
    site_title = 'Strep A Database'
    index_title = 'Database contents'

    login_template = 'database/login.html'

    def has_permission(self, request):
        # all users have implicit permission to access the admin site (because it is not just for admins)
        # although non-admin users will not be able to simply view anything other than studies/results
        return request.user.is_active and request.user.can_view_data

admin_site = StrepAAdminSite()
