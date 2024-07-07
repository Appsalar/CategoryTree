from django.urls import path
from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet, SimilarityViewSet, getByDepth, getSimilar


router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"categories/similarities", SimilarityViewSet, basename="similarity")

urlpatterns = router.urls

urlpatterns += [
    path("categories/get_by_depth/<int:depth>", getByDepth),
    path("categories/similar/<int:pk>", getSimilar),
]
