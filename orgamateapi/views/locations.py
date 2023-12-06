from rest_framework import viewsets, status, serializers
from rest_framework import serializers
from rest_framework.response import Response
from orgamateapi.models import Location

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'name']

class LocationViewSet(viewsets.ViewSet):

    def list(self, request):
        location = Location.objects.all()
        serializer = LocationSerializer(location, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location, context={'request': request})
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        name = request.data.get('name')

        create = Location.objects.create(
            name=name,
        )

        serializer = LocationSerializer(create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
    def destroy(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
            self.check_object_permissions(request, location)
            location.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)