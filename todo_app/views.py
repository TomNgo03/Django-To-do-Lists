from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ToDoList, ToDoItem

class ListListView(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = "todo_app/index.html"
    context_object_name = "todo_lists"
    
    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

class ItemListView(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"
    context_object_name = "todo_items"
    
    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class ListCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ["title"]
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add a new list"
        return context

class ItemCreate(LoginRequiredMixin, CreateView):
    model = ToDoItem
    fields = [
        "title",
        "description",
        "due_date",
    ]
    
    def form_valid(self, form):
        form.instance.todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["title"] = "Create a new item"
        return context
    
    def get_success_url(self):
        return reverse("list", args=[self.kwargs["list_id"]])

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    fields = [
        "title",
        "description",
        "due_date",
    ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit Item"
        return context
    
    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ListDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    success_url = "/"

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = ToDoItem
    
    def get_success_url(self):
        return reverse("list", args=[self.kwargs["list_id"]])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
