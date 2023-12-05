from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response

from orgamateapi.models import Task, Priority
from .priorities import PrioritySerializer


class TaskSerializer(serializers.ModelSerializer):
    priority = PrioritySerializer(many=False)

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review (this will still run the check and i dont need to add it to the fields! )
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Task
        fields = ['id','task_item', 'note', 'isComplete', 'date_added', 'priority', 'user']
     

class TaskViewSet(viewsets.ViewSet):

    def list(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request}) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    

    def create(self, request):
        task_item = request.data.get('task_item')
        note = request.data.get('note')
        priority = Priority.objects.get(pk=request.data["priority"])

        create = Task.objects.create(
            task_item=task_item,
            note=note,
            priority=priority,
            user=request.user
        )
      
        serializer = TaskSerializer(create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)

            if task.user.id != request.user.id:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            task.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)