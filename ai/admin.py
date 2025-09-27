from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import QA

@admin.register(QA)
class QAAdmin(ImportExportModelAdmin):
    list_display = ("question", "answer")