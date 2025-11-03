from django.db import models

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=100)
    rollNo = models.CharField(max_length=10)
    email = models.EmailField(blank=False)

    def __str__(self):
        return self.name


class studentDetails(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phoneNumber = models.IntegerField()

    def __str__(self):
        return self.student.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField()
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title