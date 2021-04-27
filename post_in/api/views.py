from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from notes.models import Note
from api.serializers import NoteSerializer


@api_view(['GET', 'POST'])
def notes_list(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NoteSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


