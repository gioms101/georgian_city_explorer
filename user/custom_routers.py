from rest_framework.routers import DefaultRouter


class CustomRouter(DefaultRouter):
    def get_lookup_regex(self, viewset, lookup_prefix=''):
        return ""
