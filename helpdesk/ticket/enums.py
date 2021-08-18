from django.db import models
from django.utils.translation import ugettext as _


class TicketStatuses(models.TextChoices):
    """
    Statues a ticket can have
    """
    CREATED = 'CREATED', _('Created')
    RESOLVED = 'RESOLVED', _('Resolved')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELED = 'CANCELED', _('Canceled')
    SUSPENDED = 'SUSPENDED', _('Suspended')
