from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Podcast(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="podcasts"
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="podcasts"
    )

    def __str__(self) -> str:
        return str(self.title)
