from django.conf import settings
from django.db import models, transaction


class DatasetUpload(models.Model):
    """
    Stores an uploaded CSV dataset and its summary analytics.
    Each dataset belongs to a specific user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dataset_uploads',
       
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    summary = models.JSONField(default=dict, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at', '-id']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            transaction.on_commit(
                lambda: self._prune_old_uploads(user=self.user)
            )

    @classmethod
    def _prune_old_uploads(cls, user, keep=5):
        """
        Keep only the most recent `keep` uploads PER USER.
        """
        ids_to_keep = (
            cls.objects.filter(user=user)
            .order_by('-uploaded_at', '-id')
            .values_list('id', flat=True)[:keep]
        )
        cls.objects.filter(user=user).exclude(id__in=list(ids_to_keep)).delete()

    def delete(self, *args, **kwargs):
        storage = self.file.storage
        path = self.file.name
        super().delete(*args, **kwargs)
        if path:
            storage.delete(path)