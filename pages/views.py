from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserTasks
from .forms import TaskDetails

class HomePageView(TemplateView):
    template_name = 'home.html'

class FeaturesPageView(TemplateView):
    template_name = 'features.html'

class WebappPageView(TemplateView):
    template_name = 'webapp.html'

class InboxView(LoginRequiredMixin, ListView):
    model = UserTasks
    template_name = 'inbox.html'
    login_url = 'login'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['tasks'].filter(complete=False).count()
       
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = TaskDetails
    template_name = 'create_task.html'
    success_url = reverse_lazy('inbox')
    login_url = 'login'
