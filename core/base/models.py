from auditlog.models import AuditlogHistoryField, LogEntry
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _


@auditlog.register()
class BaseHistoryModel(models.Model):
    """Main system class"""
    history = AuditlogHistoryField()

    @property
    def updated_at(self):
        """ Returns the last action different from CREATE """
        # Get the last action different from CREATE
        last = self.history.filter(action__gt=int(LogEntry.Action.CREATE)).order_by('-timestamp').first()
        return last.timestamp if last else None

    @property
    def log_history(self):
        """ Returns the list with all actions and dates """
        records = []
        for record in self.history.all():
            records.append(
                f'{LogEntry.Action.choices[record.action][1]} from {record.actor if record.actor else "system"} '
                f'at {record.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")}'
            )
        return ", ".join(records)

    class Meta:
        abstract = True


@auditlog.register()
class BaseModel(BaseHistoryModel):
    """Main system class"""
    created_at = models.DateTimeField(_("Created"), blank=False, null=False, auto_now_add=True, editable=False)
    is_active = models.BooleanField(_("Active"), blank=False, null=False, default=True, db_index=True)
    is_deleted = models.BooleanField(_("Deleted"), blank=False, null=False, default=False)

    class Meta:
        abstract = True
        ordering = ("-created_at",)
