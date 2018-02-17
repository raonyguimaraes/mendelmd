from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .models import App
# Create your views here.
def index(request):
    app_list = App.objects.all()[:5]
    context = {'app_list': app_list}
    return render(request, 'mapps/index.html', context)


class AppCreate(CreateView):
    model = App
    fields = ['name', 'status', 'category', 'repository', 'type', 'config']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)