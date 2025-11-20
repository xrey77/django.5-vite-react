from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    qrcodeurl = Base64ImageField(required=False) # 'required=False' allows partial updates (PATCH)    
    userpic = serializers.ImageField(required=False)    
    # userpic = serializers.ImageField( required=False,allow_null=True, allow_empty_file=True)
        
    class Meta:
        model = Users
        fields = '__all__' # Or specify a list of fields        
        
    # def create(self, validated_data):
    #     # Extract the custom field from validated_data (if passed via serializer.save(userpic=...))
    #     userpic = validated_data.pop('userpic', None) 
    #     instance = Pix.objects.create(**validated_data)
        
    #     if userpic:
    #         instance.userpic = userpic
    #         instance.save()
        
    #     return instance

    # # You might also need to implement the update method for updates
    # def update(self, instance, validated_data):
    #     # ... standard update logic ...
    #     userpic = validated_data.pop('userpic', None)
    #     # ... update other fields ...
    #     instance = super().update(instance, validated_data)

    #     if userpic:
    #         instance.userpic = userpic
    #         instance.save() # Manually save after changing a field outside of super().update()

    #     return instance        
