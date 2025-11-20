from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from django.db.models.functions import Lower
from django.db.models import Value

class ProductList(APIView):    
    def get(self, request, *args, **kwargs):
        page = kwargs.get('page') 
        
        queryset = Product.objects.all().order_by('id')
        serializer = ProductSerializer(queryset, many=True)  
        if not queryset.exists():        
            return Response({'message': 'No record(s) found.'}, status.HTTP_400_BAD_REQUEST)
        else:

            perpage = 5
            paginator = Paginator(queryset, perpage)
            page_obj = paginator.get_page(page)

            serialized_data = list(page_obj.object_list.values())
            
            pageData = {
                'page': page,
                'totpage': paginator.num_pages,
                'totalrecords': paginator.count,
                'products': serialized_data                
            }
            
            return Response(pageData, status.HTTP_200_OK)
        
        
        
class ProductSearch(APIView):    
    def get(self, request, *args, **kwargs):
        page = kwargs.get('page')
        key = kwargs.get('key')  
        
        queryset = Product.objects.all().order_by('id')
 
        findQuery = queryset.filter(
            descriptions__iregex=key
        )
                
        serializer_class = ProductSerializer(findQuery, many=True)         
        perpage = 5
        paginator = Paginator(findQuery, perpage)
        page_obj = paginator.get_page(page)

        serialized_data = list(page_obj.object_list.values())
        if paginator.count > 0:                
            pageData = {
                'page': page,
                'totpage': paginator.num_pages,
                'totalrecords': paginator.count,
                'products': serialized_data                
            }            
            return Response(pageData, status.HTTP_200_OK)
        
        else:
            return Response({'message': 'No record(s) found.'}, status.HTTP_400_BAD_REQUEST)
                

