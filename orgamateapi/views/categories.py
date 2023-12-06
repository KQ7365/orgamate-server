from rest_framework import viewsets, status, serializers
from rest_framework import serializers
from rest_framework.response import Response
from orgamateapi.models import Category

class CategorySerializer(serializers.ModelSerializer):

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review (this will still run the check and i dont need to add it to the fields! )
        return self.context['request'].user == obj.user
     
    class Meta:
        model = Category
        fields = ['id', 'label']

class CategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        label = request.data.get('label')

        create = Category.objects.create(
            label=label,
        )

        serializer = CategorySerializer(create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            self.check_object_permissions(request, category)
            category.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)