from django.test import TestCase
from .models import *
from .serializers import *

# Create your tests here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

class StoreRequestView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = StoreRequest.objects.all()
    serializer_class = StoreRequestSerializer

    # ... (your existing code)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Your existing validation logic for store_request_items
        request_items = request.data.get('store_request_items')
        if not type(request_items) == list or not request_items:
            return Response({'error':'store_request_items must be a list and cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Updating the StoreRequest instance
        store_request_serializer = StoreRequestSerializer(instance, data=request.data, partial=partial)
        store_request_serializer.is_valid(raise_exception=True)
        sr_data = store_request_serializer.save()

        # Updating or creating StoreRequestItem instances
        for item in request_items:
            item['store_request'] = sr_data.id
            if 'id' in item:
                # If the item has an 'id', it means it already exists, so we update it
                store_request_item = StoreRequestItem.objects.get(id=item['id'])
                serializer = StoreRequestItemSerializer(store_request_item, data=item, partial=True)
            else:
                # If the item doesn't have an 'id', it means it's a new item, so we create it
                serializer = StoreRequestItemSerializer(data=item)

            if not serializer.is_valid():
                # Rollback changes if the serializer is not valid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

        return Response({'msg':'store request updated','data': store_request_serializer.data}, status=status.HTTP_200_OK)
