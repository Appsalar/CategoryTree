from collections import deque

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from categories.models import Category, Similarity
from categories.serializers import CategorySerializer, SimilaritySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["parent_id"]


class SimilarityViewSet(ModelViewSet):
    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer


@api_view(["GET"])
def getByDepth(request, depth):
    root = Category.objects.filter(Q(parent__isnull=True))

    nodes = list(Category.objects.all())

    lastLevel = deque(root)
    for _ in range(depth):
        lastLevel = [category for category in nodes if category.parent in lastLevel]

    categories = list(lastLevel)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getSimilar(request, pk):
    get_object_or_404(Category.objects.all(), pk=pk)

    qs = Similarity.objects.filter(Q(firstCategory_id=pk) | Q(secondCategory_id=pk))
    similarCategories = [x.firstCategory if x.firstCategory_id != pk else x.secondCategory for x in qs]

    serializer = CategorySerializer(similarCategories, many=True)
    return Response(serializer.data)
