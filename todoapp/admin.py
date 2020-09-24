from django.contrib import admin
from .models import Todo

#Display the date created field on admin, since it does not display by default
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(Todo, TodoAdmin)