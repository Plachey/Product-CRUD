import os
import shutil

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from myproduct.models import Products


class TestProduct:

    def teardown(self):
        shutil.rmtree(os.path.join('test'), ignore_errors=True)

    def test_product_create(self, admin_client, post_param):
        (data, expected_status_code) = post_param

        if expected_status_code == 201:
            response = admin_client.post('/products/', data=data)

            assert response.status_code == 201
        elif expected_status_code == 400:
            response = admin_client.post('/products/', data=data)

            assert response.status_code == 400
            assert response.json()['status'] == 'Bad request'
            assert response.json()['message'] == 'Problem with data or convertation'

    def test_product_put(self, admin_client, put_param):
        image = SimpleUploadedFile(name='test_image.png',
                                   content=open(os.path.join('tests', '1.png'),'rb').read())
        product = Products.objects.create(name="Nick", description="Gogol mogol", logo=image)

        (data, expected_status_code) = put_param

        if expected_status_code == 400:
            response = admin_client.put(f'/products/{product.uuid}/',
                                        data=data, content_type='application/json')

            assert response.status_code == 400
            print('mmm', response.json())
            assert response.json()['status'] == 'Bad request'
            assert response.json()['message'] == 'Problem with data or you can update file only once'

    def test_product_get_all_data(self, admin_client):
        image = SimpleUploadedFile(name='test_image.png',
                                   content=open(os.path.join('tests', '1.png'),'rb').read())

        Products.objects.create(name="Valik", description="Gogol", logo=image)
        Products.objects.create(name="Stepa", description="Mogol", logo=image)

        response = admin_client.get('/products/')

        assert response.status_code == 200

        assert response.json()['count'] == 2
        assert response.json()['results'][0]['name'] == 'Valik'
        assert response.json()['results'][0]['description'] == 'Gogol'

        assert response.json()['results'][1]['name'] == 'Stepa'
        assert response.json()['results'][1]['description'] == 'Mogol'

    def test_product_get_modify(self, admin_client):
        image = SimpleUploadedFile(name='test_image.png',
                                   content=open(os.path.join('tests', '1.png'),
                                                'rb').read())

        Products.objects.create(name="Valik", description="Gogol", logo=image)
        Products.objects.create(name="Stepa", description="Mogol", logo=image)

        response = admin_client.get('/products/?modified=False')
        assert response.status_code == 200

        assert response.json()['count'] == 2
        assert response.json()['results'][0]['name'] == 'Valik'
        assert response.json()['results'][0]['description'] == 'Gogol'

        assert response.json()['results'][1]['name'] == 'Stepa'
        assert response.json()['results'][1]['description'] == 'Mogol'

        response = admin_client.get('/products/?modified=True')
        assert response.status_code == 200

        assert response.json()['count'] == 0

    def test_product_delete_one_and_raise_error(self, admin_client):
        image = SimpleUploadedFile(name='test_image.png',
                                   content=open(os.path.join('tests', '1.png'), 'rb').read())

        product1 = Products.objects.create(name="Valik", description="Gogol", logo=image)
        product2 = Products.objects.create(name="Stepa", description="Mogol", logo=image)

        response = admin_client.delete(f"/products/{product1.uuid}/")

        assert response.status_code == 200
        products = Products.objects.all()
        assert len(products) == 1

        response = admin_client.delete(f"/products/{product1.uuid}/")

        assert response.status_code == 404

        with pytest.raises(ValidationError):
            admin_client.delete("/products/f2322222/")


@pytest.fixture(
    params=[('put_wrong_data', 400)])
def put_param(request):
    return request.getfixturevalue(request.param[0]), request.param[1]


@pytest.fixture()
def put_wrong_data():
    return {
        "name": "Change",
        "description": "Change mogol"
    }


@pytest.fixture(
    params=[('post_data', 201), ('post_logo_data_wrong', 400)])
def post_param(request):
    return request.getfixturevalue(request.param[0]), request.param[1]


@pytest.fixture()
def post_data():
    image = SimpleUploadedFile(name='test_image.png',
                               content=open(os.path.join('tests', '1.png'), 'rb').read())
    return {
        "name": "Nick Gogol",
        "description": "Gogol mogol",
        "logo": image
    }


@pytest.fixture()
def post_logo_data_wrong():
    return {
        "name": "Nick Gogol",
        "description": "Gogol mogol",
        "logo": 'logo'
    }
