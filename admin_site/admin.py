
from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_title = 'Admin'
    site_header = 'My administration'

    def get_app_list(self, request, *args, **kwargs):
        _ = self
        app_dict = super()._build_app_dict(request)
        if not app_dict:
            return []

        if 'auth' in app_dict:
            app_dict['auth']['name'] = 'Django Auth'

        # note that dict_values is not a list.
        return list(app_dict.values())
