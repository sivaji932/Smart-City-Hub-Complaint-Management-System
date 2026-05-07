from django.db import models

class Citizen(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  
    role = models.CharField(max_length=50, default='citizen')  

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'citizen'


class Admin(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  
    role = models.CharField(max_length=50, default='admin')  

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'admin'


class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    issue = models.CharField(max_length=100)  
    description = models.TextField()
    area_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  
    user_id = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='complaints')
    date_time = models.DateTimeField(auto_now_add=True)
    complaint_status = models.CharField(max_length=50, default='open')

    def __str__(self):
        return f"{self.issue} - {self.complaint_id} by {self.user_id.username}"

    class Meta:
        db_table = 'complaint'
