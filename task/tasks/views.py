from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, RedirectView, ListView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.response import Response

from .forms import UserLoginForm, UserRegisterForm, TaskForm, EditForm, EditUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserInfo, Task
from django.db.models import Q
from .utils import MyMixin
from .serializers import TaskSerializer
from rest_framework import generics
from .permissions import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import *

class UserRegister(CreateView):
    # регистрация и авторизация
    form_class = UserRegisterForm
    template_name = 'tasks/register.html'

    def form_valid(self, form):
        form.save()
        request = self.request
        messages.success(request, 'Вы успешно зарегистрировались')
        # return redirect('auth')
        fpp = form.cleaned_data
        user = authenticate(request, username=fpp['username'], password=fpp['password1'])
        UserInfo.objects.create(user=user)
        if user and user.is_active:
            login(request, user)
            messages.success(request, 'Вы успешно авторизрвались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
            return redirect('login')

class LoginUser(LoginView):
    # авторизация
    form_class = UserLoginForm
    template_name = 'tasks/login.html'

class LogoutUser(RedirectView):
    #выход из авторизации
    permanent = False
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('auth')

class HomeTask(MyMixin, ListView):
    # отображение списка задач по условиям
    template_name = 'tasks/index.html'
    # передает в переменную object_list, но мы html используем переменную task
    context_object_name = 'task'
    paginate_by = 3
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.get_task()

class CreateTask(CreateView):
    # создание новой задачи
    form_class = TaskForm
    # raise_exception = True  #если не хотим пускать в добавление неавторизованных полтзователей а выдавать ошибку
    template_name = 'tasks/add_task.html'
    # Если в моделе есть    def get_absolute_url(self):     то перейдет по этому url
    #но если хоnим то на главную
    success_url = reverse_lazy('reset')

    def form_valid(self, form):
        #автора присвоить к новой задаче
        w = form.save(commit=False)
        w.user = self.request.user
        return super().form_valid(form)

class UpdatePage(UpdateView):
    # редактирование задачи
    model = Task
    form_class = EditForm
    template_name = 'tasks/edit_task.html'
    success_url = reverse_lazy('home')


def ResetTask(request):
    # нажимая "Задачи" идет сброc всех установок отбора и переход на "Home"
    user = request.user
    author = UserInfo.objects.get(user=user.pk)
    author.made = 0
    author.parity = 0
    author.chose = 0
    author.selection = 0
    author.selection_key = ""
    author.save()
    return redirect('home')

def SearchResultsView(request):
    # поиск задачи по заданному ключу. Задается отбор ( см. "Настройки") и далее на "home"
    query = request.GET.get('search')
    user = request.user
    author = UserInfo.objects.get(user=user.pk)
    author.selection = 1
    author.selection_key = query
    author.save()
    return redirect('home')

class SelectionTask(UpdateView):
    # нажимая "Настройки" задаем отборы для отображения задач
    model =UserInfo
    form_class = EditUserForm
    template_name = 'tasks/select_infouser.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        # info = self.request.user
        return UserInfo.objects.filter(user__pk=self.kwargs['pk'])

def DeletePage(request, pk):
    # удаление задачи
    Task.objects.filter(pk=pk).delete()

    return redirect('home')

class TaskAPIListPagination(PageNumberPagination):
    # REST пагинация для списка задач
    page_size = 3
    page_size_query_param = 'pag-size'
    max_page_size = 5

class TaskAPIList(generics.ListCreateAPIView):
    # REST список задач
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuther,)
    pagination_class = TaskAPIListPagination
    # authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        # задаем отбор задач по настройкам
        try:
            user = self.request.user
            author = UserInfo.objects.get(user=user.pk)
            task = Task.objects.filter(user=user)
            if author.made:
                task = task.filter(made=False)

            if author.parity:
                task = task.filter(parity=True)

            if author.chose:
                task = task.filter(chose=True)

            if author.selection:
                task = task.filter(
                    Q(title__icontains=author.selection_key) | Q(content__icontains=author.selection_key))

            if author.sorted:
                task = task.order_by('performance', '-parity')
            else:
                task = task.order_by('-parity', 'performance')

            return task
        except:
            return Response({'error': 'Нет доступа. авторизуйтесь'})

class TaskAPIUpdate(generics.RetrieveUpdateAPIView):
    # REST редактирование задачи данного пользователя
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuther, IsAdminUser)
    # authentication_classes = (TokenAuthentication, )

class TaskAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
# class TaskAPIDetailView(generics.DestroyAPIView):
    # REST удаление задачи данного пользователя
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuther , IsAdminUser)

class LogoutView(RedirectView):
    # REST выход с авторизации и переход на задание авторизации
    http_method_names = ["get", "post", "options"]
    permission_classes = [permissions.IsAuthenticated]
    url = reverse_lazy('auth')

    # def get(self, request):
    #     logout(request)
    #     return redirect('drf-auth/login/')