from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from orgamateapi.models import Priority, Location, Item, Category
from .locations import LocationSerializer
from .categories import CategorySerializer
from .tags import TagSerializer
from .notes import NoteSerializer

class ItemSerializer(serializers.ModelSerializer):
    noteItemId = NoteSerializer(many=True)
    category = CategorySerializer(many=False)
    location = LocationSerializer(many=False)
    tags = TagSerializer(many=True)

    def get_is_owner(self, obj):
        # Check if the user is the owner of the task (this will still run the check and i dont need to add it to the fields! )
        return self.context['request'].user == obj.user
    
    class Meta:
        model = Item
        fields = ['id', 'image', 'name', 'description', 'category', 'location', 'tags', 'user', 'noteItemId']
        #Note to self: noteItemId was so when we want to view an item details, we see attributed notes. I had it the other way around and thats incorrect. It creates whats called a
        #circular serialization
class ItemViewSet(viewsets.ViewSet):
    
    def list(self, request):
        # Filter tasks based on the current user
        item = Item.objects.filter(user=request.user)
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        image = request.data.get('image')
        name = request.data.get('name')
        description = request.data.get('description')
        category = Category.objects.get(pk=request.data["category"])
        location = Location.objects.get(pk=request.data["location"])

        create = Item.objects.create(
            image=image,
            name=name,
            description=description,
            category=category,
            location=location,
            user=request.user
        )

        tag_ids = request.data.get('tags', [])
        create.tags.set(tag_ids)

        serializer = ItemSerializer(create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)

            if item.user.id != request.user.id:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        