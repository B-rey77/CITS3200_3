from django.contrib import admin

class StrepAAdminSite(admin.AdminSite):
    site_header = 'Strep A Database'
    site_title = 'Strep A Database'
    index_title = 'Database contents'

    login_template = 'database/login.html'

admin_site = StrepAAdminSite()
