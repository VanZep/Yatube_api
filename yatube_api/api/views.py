from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404

from posts.models import Post, Group
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Представление постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrIsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrIsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrIsAuthenticatedOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowCreateListViewSet(
    CreateModelMixin, ListModelMixin, viewsets.GenericViewSet
):
    """Представление подписчиков."""

    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
