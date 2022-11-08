from django.db import models

# Create your models here.

class Tiket(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    repoURL = models.TextField()
    branch = models.TextField()
    status = models.TextField()
    create_date = models.DateTimeField()
    def __str__(self):
        return self.subject

class Thred(models.Model):
    tiket = models.ForeignKey(Tiket, on_delete=models.CASCADE)
    content = models.TextField()
    psalmResult = models.TextField()
    checkResult = models.CharField(max_length=20)
    create_date = models.DateTimeField()