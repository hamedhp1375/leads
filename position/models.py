from django.db import models


# Create your models here.
class Lead(models.Model):
    status_choices = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=status_choices, default='new')

    class Meta:
        db_table = 'lead'
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created']


class ActionHistory(models.Model):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'action_history'
        verbose_name = 'Action History'
        verbose_name_plural = 'Action Histories'
        ordering = ['-created']

