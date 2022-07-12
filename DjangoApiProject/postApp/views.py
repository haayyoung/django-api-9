from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import PostSerializer
from .models import Post

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all() 

        serializer = PostSerializer(posts, many=True) 
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data) 
        
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class PostDetail(APIView):
    def get_object(self, postId):
        try:
            return Post.objects.get(pk=postId)
        except Post.DoesNotExist: 
            raise Http404
    
    def get(self, request, postId, format=None):
        post = self.get_object(postId)
        serializer = PostSerializer(post)
        return Response(serializer.data)