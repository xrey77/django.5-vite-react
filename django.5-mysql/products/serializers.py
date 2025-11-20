from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','category','descriptions','qty','unit','costprice','sellprice','saleprice','productpicture','alertstocks','criticalstock',)
        # fields = '__all__'
