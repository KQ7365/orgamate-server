from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response

from orgamateapi.models import Priority

class PrioritySerializer(serializers.ModelSerializer):

    class Meta:
        model = Priority
        fields = ['id', 'label']

class PriorityViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        tasks = Priority.objects.all()
        serializer = PrioritySerializer(tasks, many=True, context={'request': request}) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self, request, pk=None):
        try:
            priority = Priority.objects.get(pk=pk)
            serializer = PrioritySerializer(priority, context={'request': request})
            return Response(serializer.data)
        except Priority.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        label = request.data.get('label')

        create = Priority.objects.create(
            label=label
        )

        serializer = PrioritySerializer(create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)