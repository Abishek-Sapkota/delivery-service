import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    """
        The Profile model is a Django model that extends the TimeStampedModel class. It contains the following fields:
    Args:
        user (str): a one-to-one relationship with the User model, which is the primary key for the profile.
        first_name (str): a character field for the first name of the user.
        middle_name (str): a character field for the middle name of the user.
        last_name (str): a character field for the last name of the user.
        dob_english (date): a date field for the date of birth of the user.
        blood_group (str): a character field for the blood group of the user.
        image (image): an image field to store the profile picture of the user.
        qr_code_content (str): a text field to store the QR code content for the user.
        contact_number (str): a character field for the contact number of the user.
        email (str): an email field to store the email address of the user.
    Meta:
        The Meta class contains the verbose_name and verbose_name_plural attributes, which specify the human-readable names for
        the model and its plural form.

    Note that this model is related to the User model through a one-to-one relationship, which means that each User instance has
    one and only one associated Profile instance.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("Username"),
        max_length=255,
        unique=True,
        null=False,
    )
    mobile_number = models.CharField(
        _("Mobile Number"),
        max_length=15,
        null=False,
        unique=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile_number"]
    EMAIL_FIELD = "email"

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return self.email

class Profile(models.Model):
    """
        This model represents the OTP (one-time password) data associated with a user. It has the following fields:

    Args:
        uu_id (uuid): A string field that stores a UUID value.
        user (str): A foreign key that associates a User object with the OTP.
        otp(str): A string field that stores the OTP value.
        activation_key(str): A string field that stores an activation key for the OTP.
        This model also inherits from TimeStampedModel, which adds the following fields to the model:
        created (date): A DateTimeField that stores the creation time of the object.
        modified (date): A DateTimeField that stores the last modification time of the object.

    Method:
        The __str__ method of the UserOtp class returns the email of the associated User object.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    dob_english = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="user/profile", null=True, blank=True)
    qr_code_content = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"