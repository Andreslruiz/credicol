from django.db import models


class ColombiaDepartments(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ColombiaCities(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey('ColombiaDepartments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
