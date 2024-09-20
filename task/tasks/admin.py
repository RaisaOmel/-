from django.contrib import admin
from .models import Task
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'parity', 'performance', 'made', 'content', 'chose')
    list_display_links = ('id','title')
    fields = [('title','performance'),  'content',('made', 'parity', 'chose')]
    search_fields = ('title','content')
    list_editable = ('parity','made','chose')
    list_filter = ('performance','made','parity','chose')
    list_per_page = 10
    ordering = ('-parity','performance','title')
    actions = ['set_not_made','set_made','set_not_parity','set_parity']
    save_on_top = True

    @admin.action(description='Сделано')
    def set_made(self, request, queryset):
        kol = queryset.update(made=1)
        self.message_user(request, f'Выполнено {kol}')

    @admin.action(description='Не сделано')
    def set_not_made(self, request, queryset):
        kol = queryset.update(made=0)
        self.message_user(request, f'Выполнено {kol}')

    @admin.action(description='неважнно')
    def set_not_parity(self, request, queryset):
        kol = queryset.update(parity=0)
        self.message_user(request, f'Выполнено {kol}')

    @admin.action(description='важнно')
    def set_parity(self, request, queryset):
        kol = queryset.update(parity=1)
        self.message_user(request, f'Выполнено {kol}')

admin.site.register(Task, TaskAdmin)
# Register your models here.

admin.site.site_title = 'Управление'
admin.site.site_header = 'Ежедневник'
