from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404


from .models import App
# Create your views here.
def index(request):
    
    if request.method == 'POST':
        apps = request.POST.getlist('apps')
        action = request.POST['action']
        for app_id in apps:
            if request.user.is_staff:
                app = get_object_or_404(App, pk=app_id)
            else:
                app = get_object_or_404(App, pk=app_id, user=request.user)
        
            if action == "delete":
                app.delete()

    app_list = App.objects.all()[:5]
    context = {'app_list': app_list}
    return render(request, 'mapps/index.html', context)


class AppCreate(CreateView):
    model = App
    fields = ['name', 'status', 'category', 'source', 'repository', 'type', 'config', 'main', 'install']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AppUpdate(UpdateView):
    model = App
    fields = ['name', 'status', 'category', 'source', 'repository', 'type', 'config', 'main', 'install']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
