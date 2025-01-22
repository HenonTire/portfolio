from django.db import models

class Schedule(models.Model):
    name = models.CharField(max_length=10)
    contact = models.JSONField(max_length=100)
    message = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return f"{self.name} - {self.message}"

 