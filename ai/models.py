from django.db import models

class QA(models.Model):
    question = models.CharField(max_length=500)  # unique=True সরানো হয়েছে
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.question