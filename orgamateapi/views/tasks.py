from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response

from orgamateapi.models import Task


class TaskSerializer(serializers.ModelSerializer):
    #TODO: Will need to serialize priority field within here since its FK because right now will only show ID


    def get_is_owner(self, obj):
        # Check if the user is the owner of the review (this will still run the check and i dont need to add it to the fields! )
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Task
        fields = ['id','task_item', 'note', 'label', 'isComplete', 'date_added', 'priority']
     

class TaskViewSet(viewsets.ViewSet):

    def list(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request}) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)