from django.db import models
from django.utils import timezone
# Create your models here.

class Room(models.Model):
    room_no=models.IntegerField(unique=True)
    
    @property
    def capacity(self):
        if 101 <= self.room_no < 150:
            return 1
        elif 201 <=self.room_no < 250:
            return 2
        elif 301 <=self.room_no < 350:
            return 3
        return 0
    
    @property
    def occupied(self):
        return Booking.objects.filter(room=self,is_confirmed=True).count()
    
    @property
    def available(self):
        return self.capacity-self.occupied

    def __str__(self):
        return f"Room{self.room_no} ({self.capacity()}-in-1)"

class Student(models.Model):
    name=models.CharField(max_length=100)
    reg_no=models.CharField(max_length=20,unique=True)
    email=models.EmailField()
    
    def __str__(self):
        return f"{self.name} -> {self.reg_no}"

class Booking(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    is_confirmed=models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.student.name} -> {self.room.room_no}"
    



            