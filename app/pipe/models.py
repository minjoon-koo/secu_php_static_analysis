from django.db import models

# Create your models here.

class Tiket(models.Model):
    jira_tiket = models.TextField(null=True)
    status = models.TextField()
    create_date = models.DateTimeField()
    jira_id = models.TextField(null=True)
    pr_num = models.TextField()
    pr_exec = models.TextField()


class Thred(models.Model):
    tiket = models.ForeignKey(Tiket, on_delete=models.CASCADE)
    thred_num = models.CharField(max_length=10,null=True)
    content = models.TextField()
    psalmResult = models.TextField()
    checkResult = models.CharField(max_length=20)
    create_date = models.DateTimeField()

class Result(models.Model):
    tiket = models.ForeignKey(Tiket, on_delete=models.CASCADE)
    thred = models.CharField(max_length=10)
    Type = models.CharField(max_length=20)
    file_name = models.TextField()
    line_from = models.CharField(max_length=10)
    line_to = models.CharField(max_length=10)
    snippet = models.TextField()
    messages = models.TextField()
    link = models.TextField()
    taint_trace = models.TextField()

class Info(models.Model):
    tiket = models.ForeignKey(Tiket, on_delete=models.CASCADE)
    branch = models.TextField()
    repoURL = models.TextField()
    content = models.TextField()