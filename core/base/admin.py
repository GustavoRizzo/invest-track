import csv
import logging

from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, path
from django.utils.html import format_html

logger = logging.getLogger(__name__)


class CommonInline(admin.TabularInline):
    min_num = 0
    max_num = 1
    extra = 0
    can_delete = False
    exclude = ('id', 'created_at', 'modified_at', 'deleted_at',
               'audit', 'hash_id', 'is_active', 'is_deleted')


class BaseAdmin(admin.ModelAdmin):
    list_display = ()
    search_fields = ()
    list_filter = ("is_active",)
    readonly_fields = ("created_at", 'log_history',)
    header_list = {}
    extra_header_list = ()
    exclude_csv_fields = ("created_at",)
    extra_csv_fields = ()
    actions = [
        "export_selected_objects_via_csv",
        "export_filtered_objects_via_csv",
        "export_all_objects_via_csv",
    ]
    fieldsets = (
        (_('Other values'), {
            # 'classes': ('collapse',),
            'fields': (('is_active', 'is_deleted'), 'created_at', 'log_history',),
        }),
    )
    # Used to add the fieldsets
    edit_fields = None
    add_fieldsets = None

    def get_actions(self, request):
        """
        Add the 'Delete' option from commands list only for the super user
        """
        actions = super().get_actions(request)
        if "delete_selected" in actions and not request.user.is_superuser:
            del actions["delete_selected"]
        return actions

    def export_selected_objects_via_csv(self, request, queryset):
        # Send response
        return self.export_objects_via_csv(request, queryset)

    def export_filtered_objects_via_csv(self, request, queryset):
        # Export all records using current filters
        cl = self.get_changelist_instance(request)
        records = cl.get_queryset(request)
        # Do the job
        return self.export_objects_via_csv(request, records)

    def export_all_objects_via_csv(self, request, queryset):
        # Export all records
        records = self.get_queryset(request)
        # Do the job
        return self.export_objects_via_csv(request, records)

    def export_objects_via_csv(self, request, records):
        # Do the job
        file_name = f"{self.model.__name__.lower()}-{now().date()}"
        # Put as text file to force Excel open the import dialog to chose UTF-8
        response = HttpResponse(content_type="text/csv", charset="utf-8")
        response["Content-Disposition"] = 'attachment; filename="%s.csv"' % file_name
        # The CSV writer
        writer = csv.writer(response, delimiter=";", quoting=csv.QUOTE_ALL)
        # Write a first row with header information
        headers = [
            header if header not in self.header_list else self.header_list[header]
            for header in self.list_display
            if header not in self.exclude_csv_fields
        ]
        for header in self.extra_header_list:
            headers.append(header)
        writer.writerow(headers)
        # Write data rows
        for record in records:
            values = []
            for field in self.list_display:
                if field not in self.exclude_csv_fields:
                    value = getattr(record, field)
                    # Convert lists into a sequence of values
                    if value is not None and type(value) is list:
                        value = ", ".join(value)
                    values.append(value)
            for field in self.extra_csv_fields:
                values.append(getattr(record, field)())
            writer.writerow(values)
        # Set the right message
        if len(records) == 1:
            message_bit = "1 record was"
        else:
            message_bit = "%s records were" % len(records)
        self.message_user(request, "%s successfully exported." % message_bit)
        # Send response
        return response

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # Check if the edit_fields is set
        if self.edit_fields:
            fields = ((_('Fields'), {'fields': self.edit_fields}),)
            self.fieldsets = fields + self.fieldsets
        elif self.add_fieldsets:
            self.fieldsets = self.add_fieldsets + self.fieldsets
        else:
            # Remove the fieldsets
            self.fieldsets = None
        # Check for the readonly_fields
        if self.readonly_fields:
            self.readonly_fields += ('created_at', 'log_history',)

    class Media:
        css = {'all': ('css/admin.css',)}

    class Meta:
        abstract = True
        ordering = ('-created_at',)
