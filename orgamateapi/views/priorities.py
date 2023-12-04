from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response

from orgamateapi.models import Priority

class PrioritySerializer(serializers.ModelSerializer):

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review (this will still run the check and i dont need to add it to the fields! )
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Priority
        fields = ['id', 'label']

class PriorityViewSet(viewsets.ViewSet):
    pass
#TODO: May want to do a PR and then finish this out. Need to post 3 priorities so I can then finish Task!