from django.shortcuts  import render,redirect
from .models import Task
from .forms import TodoForms
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    tasks = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date = request.POST.get('date', '')
        newtask=Task(name=name,priority=priority,date=date)
        newtask.save()
    return render(request,'home.html',{'task':tasks})

#def details(request):

#    return render(request,'details.html')

class Tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task1'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

def get_success_url(self):
    return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})
class TaskDeleteView(DetailView):
    model = Task
    template_name = 'delete.html'
    success_url=reverse_lazy('cbvhome')

def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method =='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task=Task.objects.get(id=id)
    f=TodoForms(request.POST or None,instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':task})


