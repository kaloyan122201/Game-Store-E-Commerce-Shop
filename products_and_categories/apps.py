from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products_and_categories'

class ProductsCategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products_and_categories'

    def ready(self):
        import products_and_categories.signals