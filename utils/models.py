import uuid

from model_utils.models import TimeStampedModel
from django.db import models
from django.contrib.auth import get_user_model
from utils.middlewares import get_current_user

User = get_user_model()


class TimeStampWithCreatorModel(TimeStampedModel):
    id = models.UUIDField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    """
    Abstract base class with a creation
    and modification date and time
    """

    class Meta:
        abstract = True

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_constraint=False,
        editable=False,
        related_name='created_%(class)ss',
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_constraint=False,
        editable=False,
        related_name='updated_%(class)ss',
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.created_by and get_current_user().is_authenticated:
            self.created_by_id = get_current_user().id
        if get_current_user():
            self.updated_by_id = get_current_user().id
        super(TimeStampWithCreatorModel, self).save(*args, **kwargs)

    save.alters_data = True
