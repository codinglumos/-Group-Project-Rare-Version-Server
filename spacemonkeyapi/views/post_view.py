from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from spacemonkeyapi.models import Post, Author


class PostView(ViewSet):
    # View Single Post
    def retrieve(self, request, pk):
        """Handle GET requests for single post type

        Returns:
            Response -- JSON serialized post type
        """
        post_view = Post.objects.get(pk=pk)
        serialized = PostSerializer(post_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all Post
    def list(self, request):
        """Handle GET requests to get all post types

        Returns:
            Response -- JSON serialized list of post types
        """
        post_view = Post.objects.all()
        serialized = PostSerializer(post_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    # Create a Post
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        #~ these will need to be updated once the Authentication is Running.
        # author = Author.objects.get(user=request.auth.user)
        # category = Catergory.objects.get(pk=request.data["category"])

        post = Post.objects.create(
            author=request.data["author"],
            # category=category,
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            image_url=request.data["image_url"],
            content=request.data["content"],
            approved=request.data["approved"],
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # Edit Post
    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        # category = Catergory.objects.get(pk=request.data["category"])
        # post.category = request.data["category"]
        
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)  


    # Delete Post
    def destroy(self, request, pk):
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author','title', 'publication_date', 'image_url', 'content', 'approved')