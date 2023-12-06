from rest_framework import viewsets, status, serializers
from rest_framework import serializers
from rest_framework.response import Response
from orgamateapi.models import Tag

class TagSerializer(serializers.ModelSerializer):   

   class Meta:
      model = Tag
      fields = ['id', 'label']

class TagViewSet(viewsets.ViewSet):
   
    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
   
    def retrieve(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        label = request.data.get('label')

        create = Tag.objects.create(
            label=label,
        )

        serializer = TagSerializer(create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            self.check_object_permissions(request, tag)
            tag.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
       