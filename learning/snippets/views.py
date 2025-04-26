from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from .permission import Danger
from rest_framework.exceptions import PermissionDenied
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.contrib.sessions.models import Session

'''@csrf_exempt

def snippet_list(request):
    """
    List all ccode snippets, or create a new snippet.

    """
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many = True)
        return JsonResponse(serializer.data, safe = False)
    
    elif request.method == 'POST':
        data = request.data
        serializer = serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status = 201)
        return JsonResponse(serializer.errors, status = 400)
    
@csrf_exempt

def snippet_detail(request, pk):

    """
    Retrive, update or delete a code snippet.

    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status = 400)
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status = 400)
    elif request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status = 204)  '''

#api view
  
'''@api_view(['GET','POST'])

def snippet_list(request):
    """
    List all code snippets, or create a new snippet

    """
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many = True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = request.data
        serializer = SnippetSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_created)
        return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)



def get_objects(pk):
    try:
        return Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET','PUT','DELETE'])
def snippet_detail(request, pk):

    if request.method == 'GET':
        snippet = get_objects(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    if request.method == 'PUT':
        data = request.data
        snippet = get_objects(pk)
        serializer = SnippetSerializer(snippet, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        snippet = get_objects(pk)
        snippet.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)'''
@api_view(['GET'])

def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'snippets': reverse('snipper-list', request=request)
    })

# Geniric views, Mixin

class Snippet_list(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

    def get(self, request, *args,**kwargs):
        list= self.list(request,*args,**kwargs)
        snippet = self.get_queryset().filter(title="")
        
        for i in snippet:
            i.title = "Please give a title. This is the default title"

        if snippet:
            Snippet.objects.bulk_update(snippet,['title'])                         
        return list
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(owner = self.request.user)

        
    
class Snippet_detail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        response =  self.retrieve(request, *args, **kwargs)
        #print(response.data['language'])
        
        return response

    def put(self, request, *args, **kwargs):
        #data = request.data.copy()
        #print(data)
        snippet = self.get_object()
        #print(snippet.owner)
        #print(request.user)
        if(snippet.owner != request.user):
            raise PermissionDenied("You do not have permission to edit this snippet.")
        return self.update(request, *args, **kwargs)
    
           
    def delete(self, request, *args, **kwargs):
        snippet = self.get_object()
        print(snippet)
        if snippet.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this snippet.")
        if snippet.style == "friendly":
            return Response({"detail": "Deletion is not allowed for friendly snippets."}, status=status.HTTP_403_FORBIDDEN)
        d = self.destroy(request)
        return d
    
class UserList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Danger]

    def get(self,request):
        return self.list(request)
    
class UserDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Danger]

    def get(self, request, *args, **kwargs):

        return self.retrieve(request,*args, **kwargs)
    
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        if not request.session.get('username'):
            request.session['username'] = request.user.username
        self.get_session_id(request)
        snippet = self.get_object()
        return Response(snippet.highlited)
    
    def get_session_id(self, request):
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        username = request.session.get('username')
        session = Session.objects.get(session_key = session_id)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if user_id:
            user = Snippet.objects.get(id = user_id)
            username = user.owner
        
        print(session_id,username)

        




    