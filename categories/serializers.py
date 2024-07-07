from rest_framework.serializers import ModelSerializer

from categories.models import Category, Similarity


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "parent"]


class SimilaritySerializer(ModelSerializer):
    class Meta:
        model = Similarity
        fields = ["id", "firstCategory", "secondCategory"]

    def create(self, validated_data):
        minValue, maxValue = self._getMinMaxById(validated_data)
        return Similarity.objects.create(
            firstCategory=minValue, secondCategory=maxValue
        )

    def update(self, instance, validated_data):
        minValue, maxValue = self._getMinMaxById(validated_data)
        instance.firstCategory = minValue
        instance.secondCategory = maxValue
        return instance

    def _getMinMaxById(self, validated_data):
        a, b = validated_data["firstCategory"], validated_data["secondCategory"]
        return (a, b) if a.id < b.id else (b, a)
