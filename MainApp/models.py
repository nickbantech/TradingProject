from django.db import models
class File(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    opens = models.CharField(max_length=100)
    high = models.CharField(max_length=100)
    low = models.CharField(max_length=100)
    closes = models.CharField(max_length=100)
    datetime = models.CharField(max_length=100)
    def __str__(self):
        return self.id