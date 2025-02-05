
from django.db import models

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    recipient_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    package_details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for {self.recipient_name} - {self.status}"
