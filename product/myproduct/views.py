import logging
from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Products
from .serializers import ProductsSerializer, ProductsUpdateSerializer
from .tasks import async_save

logger = logging.getLogger(__name__)


class ProductsView(viewsets.GenericViewSet):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()

    def list(self, request):
        modified = request.query_params.get('modified')
        logger.info('List Modified: {}'.format(modified))

        if modified == 'True':
            query = Products.objects.filter(updated__isnull=False)
        elif modified == 'False':
            query = Products.objects.filter(updated__isnull=True)
        else:
            query = Products.objects.all()

        logger.info('List query: {}'.format(query))
        page = self.paginate_queryset(query)
        serializer = ProductsUpdateSerializer(page, many=True)
        logger.info('List serialize: {}'.format(serializer.data))
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Products, uuid=pk)
        logger.info('Retrieve product: {}'.format(product))

        serializer = ProductsUpdateSerializer(product)
        logger.info('Retrieve serializer: {}'.format(serializer.data))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProductsSerializer(data=request.data)
        logger.info('Create request data: {}'.format(request.data))

        if serializer.is_valid():
            serializer.validated_data['logo'] = None
            serializer.save()

            logger.info('Create serializer: {}'.format(serializer.data))
            async_save(request.data['logo'], serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Problem with data or convertation'
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = get_object_or_404(Products, uuid=pk)
        logger.info('Update product: {}'.format(product))
        logger.info('Update request data: {}'.format(request.data))

        serializer = ProductsUpdateSerializer(product, data=request.data)
        if serializer.is_valid() and product.updated is None:
            serializer.validated_data['updated'] = datetime.today().strftime('%Y-%m-%d')
            serializer.validated_data['logo'] = None
            serializer.save()

            logger.info('Update serializer: {}'.format(serializer.data))

            async_save(request.data['logo'], serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.info('Update error')
        return Response({
            'status': 'Bad request',
            'message': 'Problem with data or you can update file only once'
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = get_object_or_404(Products, uuid=pk)
        logger.info('Destroy object: {}'.format(product))
        product.delete()
        logger.info('Success destroy')
        return Response(status=status.HTTP_204_NO_CONTENT)
