from django.urls import path
from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet, SimilarityViewSet, getByDepth, getSimilar


router = DefaultRouter()

router.register(r"categories", CategoryViewSet)
router.register(r"categories/similarities", SimilarityViewSet)

urlpatterns = router.urls

urlpatterns += [
    path("categories/get_by_depth/<int:depth>", getByDepth),
    path("categories/<int:pk>/similar", getSimilar),
]
