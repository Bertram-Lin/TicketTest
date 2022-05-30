from django.db import models

# Create your models here.
class Mood(models.Model):
    status = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.status

class Post(models.Model):
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='不願意透漏身分的人')
    message = models.TextField(null=False)
    del_pass = models.CharField(max_length=10)
    pub_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class PermissionRole(models.Model):
    Role = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.Role

class login(models.Model):
    user_id = models.CharField(max_length=10, default='A123456')
    password = models.CharField(max_length=10)
    PermissionRole = models.ForeignKey('PermissionRole', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id

class Severitys(models.Model):
    severity = models.CharField(max_length=10, default='不嚴重')

    def __str__(self):
        return self.severity

class Prioritys(models.Model):
    priority = models.CharField(max_length=10, default='不急')

    def __str__(self):
        return self.priority

class ticket(models.Model):
    tid = models.AutoField(primary_key = True)
    Summary = models.CharField(max_length=10, default='Bug')
    Description = models.TextField(null=False)
    Severity = models.ForeignKey('Severitys', on_delete=models.CASCADE, null=True)
    Priority = models.ForeignKey('Prioritys', on_delete=models.CASCADE, null=True)
    isResolve = models.BooleanField(default=False)

    def __str__(self):
        return self.Summary