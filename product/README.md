## Product project with CRUD Products asynchrone save logo and rotate fields

## Prepare
1) choose dev or prod and use:

-- export DJANGO_SETTINGS_MODULE=product.settings.dev_settings - dev

-- export DJANGO_SETTINGS_MODULE=product.settings.prod_settings - prod
2) python manage.py migrate
3) python manage.py runserver

## For testing
1) export DJANGO_SETTINGS_MODULE=tests.test_settings - test
2) pytest

## urls:
1) /products/ - create product 

example: {'name': 'name', 'description': 'sth', 'logo': 'choose image'}

2) /products/?modified=True/ - get list modified = True or False
3) /products/uuid/ - get detail products using uuid
4) /products/uuid/ - delete product using uuid

PS: added more if for list to show all data without (modified)
and serializer_class, queryset for use web drf api. Few settings for 
future.
