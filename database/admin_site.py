from django.contrib import admin

class StrepAAdminSite(admin.AdminSite):
	site_header = 'Strep A Database'
	site_title = 'Strep A Database'
	index_title = 'Database contents'

	login_template = 'database/login.html'

	def has_permission(self, request):
		# all users have implicit permission to access the admin site (because it is not just for admins)
		# although non-admin users will not be able to simply view anything other than studies/results
		return request.user.is_active #and request.user.can_view_data

	def get_app_list(self, request):
		"""
		Return a sorted list of all the installed apps that have been
		registered in this site.
		"""
		ordering = {
			"Userss": 1,
			"Studies": 2,
			"Results": 3
		}
		app_dict = self._build_app_dict(request)
		
		# Sort the apps alphabetically.
		app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

		# Sort the models alphabetically within each app.
		for app in app_list:
			app['models'].sort(key=lambda x: ordering[x['name']])

		return app_list

admin_site = StrepAAdminSite()
