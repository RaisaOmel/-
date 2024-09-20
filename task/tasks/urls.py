from django.urls import path, include
from .views import *

urlpatterns = [
    # список задач по заданному отбору в настройках
    path('', HomeTask.as_view(), name='home'),
    # задание отбора при нажатии "Настройки"
    path('selection/<int:pk>/', SelectionTask.as_view(), name='selection'),
    # добавление задачи
    path('add-task/', CreateTask.as_view(), name='add_task'),
    # поиск задач по ключу (текст в поиске)
    path('search/', SearchResultsView, name='search'),
    # удаление задачи
    path('delete/<int:pk>', DeletePage),
    # сброс отбора ("настройки"). после выбает полный список задач пользователя, т.е. переходит на "Home"
    path('reset/', ResetTask, name='reset'),
    # редактирование статьи
    path('task/<int:pk>', UpdatePage.as_view(), name='edit'),
    # регистрация и авторизация
    path('register/', UserRegister.as_view(), name='register'),
    # авторизация
    path('auth/', LoginUser.as_view(), name='auth'),
    # выход из авторизации
    path('logout/', LogoutUser.as_view(), name='logout'),
    # REST список задач
    path('tasklist/', TaskAPIList.as_view()),
    # REST редактирование задачи
    path('tasklist/update/<int:pk>/', TaskAPIUpdate.as_view()),
    # REST удаление задачи
    path('tasklist/delete/<int:pk>/', TaskAPIDetailView.as_view()),
    # REST авторизация и выход из пользователя
    path('drf-auth/logout/', LogoutView.as_view(), name='logoutAPI'),
    path('drf-auth/', include('rest_framework.urls')),
]

