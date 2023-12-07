from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from orgamateapi.models import Note, Item
from .items import ItemSerializer

class NoteSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False)

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Note
        fields = ['id', 'item', 'comment', 'date', 'user' ]

class NoteViewSet(viewsets.ViewSet):
    
    def list(self, request):
        # Filter tasks based on the current user
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True, context={'request': request}) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self, request, pk=None):
        try:
            note = Note.objects.get(pk=pk)
            serializer = NoteSerializer(note, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        item = Item.objects.get(pk=request.data['item'])
        # Create a new instance of a review and assign property
        note = Note()
       
        note.item = item
        note.comment = request.data['comment']
        note.user = request.auth.user
        note.save()

        try:
            serializer = NoteSerializer(note, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        try:
            note = Note.objects.get(pk=pk)

            if note.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            note.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        