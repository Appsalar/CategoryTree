from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to="images/")
    parent = models.ForeignKey(
        "self",
        related_name="children_set",
        null=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if self.parent is None and Category.objects.filter(parent__isnull=True).exists():
            raise ValueError("There can be only one root in the tree")

        if self.parent and self.parent_id == self.id:
            raise ValueError("Categories should have parents different than itself")
        super().save(*args, **kwargs)


class Similarity(models.Model):
    firstCategory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category1")
    secondCategory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category2")

    class Meta:
        indexes = [
            models.Index(fields=["firstCategory"], name="first_category_index"),
            models.Index(fields=["secondCategory"], name="second_category_index"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["firstCategory", "secondCategory"], name="similarity_uniqueness"),
            models.CheckConstraint(
                check=models.Q(firstCategory_id__lt=models.F("secondCategory_id")),
                name="firstCategory_id_lt_secondCategory_id",
            ),
        ]
