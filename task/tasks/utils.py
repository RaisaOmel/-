from django.http import HttpResponseRedirect
from .models import Task, UserInfo
from django.db.models import Q

class MyMixin(object):
    #передает список задач по условиям отбора
    def get_task(self):
        user = self.request.user
        try:
            author = UserInfo.objects.get(user=user.pk)
        except:
            # для superuser создает отборы (сработает 1раз)
            author = UserInfo.objects.create(user=user.pk)

        task = Task.objects.all().filter(user=user.pk)
        #пробавала делать отборы через перечисления (не удалось заполнять форму из бд и получить данный с формы в бд
        # if author.made == 1:
        #     task = task.filter(made=False)
        # elif author.made == 2:
        #     task = task.filter(made=True)
        #
        # if author.parity == 1:
        #     task = task.filter(parity=True)
        # elif author.parity == 2:
        #     task = task.filter(parity=False)
        #
        # if author.chose == 1:
        #     task = task.filter(chose=True)
        # elif author.chose == 2:
        #     task = task.filter(chose=False)
        #
        # if author.selection == 2:
        #     task = task.filter(performance__lte=author.selection_date)
        # elif author.selection == 1:
        #     task = task.filter(Q(title__icontains=author.selection_key) | Q(content__icontains=author.selection_key))
        if author.made:
            task = task.filter(made=False)

        if author.parity:
            task = task.filter(parity=True)

        if author.chose:
            task = task.filter(chose=True)

        if author.selection:
            task = task.filter(Q(title__icontains=author.selection_key) | Q(content__icontains=author.selection_key))

        if author.sorted:
            task = task.order_by('performance', '-parity')
        else:
            task = task.order_by('-parity', 'performance')

        return task
