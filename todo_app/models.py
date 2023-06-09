from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from django.urls import reverse
# Create your models here.

def one_week_hence():
    return timezone.now() + timezone.timedelta(days = 7)

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100, unique = True)
    
    def get_absolute_url(self):
        return reverse("list", args = [self.id])
    
    def _str_(self):
        return self.title

class ToDoItem(models.Model):
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    created_date = models.DateTimeField(auto_now_add = True)
    due_date = models.DateTimeField(default = one_week_hence)
    todo_list = models.ForeignKey(ToDoList, on_delete = models.CASCADE)
    is_done = models.BooleanField(default = False)
    
    def get_absolute_url(self):
        return reverse("item update", args = [str(self.todo_list.id), str(self.id)])
    
    def _str_(self):
        return f"{self.title}: due {self.due_date}"
    
    class Meta:
        ordering = ["due_date"]
    

