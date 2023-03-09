from django.db import models

class Search(models.Model):
    zip_code = models.IntegerField()

    def __str__(self):
        return self.zip_code