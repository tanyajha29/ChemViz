from django.db import models, transaction


class DatasetUpload(models.Model):
    """
    Stores an uploaded CSV dataset and its summary analytics.
    """

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
            transaction.on_commit(self._prune_old_uploads)

    @classmethod
    def _prune_old_uploads(cls, keep=5):
        """
        Keep only the most recent `keep` uploads (global).
        """
        ids_to_keep = (
            cls.objects.order_by('-uploaded_at', '-id')
            .values_list('id', flat=True)[:keep]
        )
        cls.objects.exclude(id__in=list(ids_to_keep)).delete()

    def delete(self, *args, **kwargs):
        """
        Ensure the stored file is removed when the record is deleted.
        """
        storage = self.file.storage
        path = self.file.name
        super().delete(*args, **kwargs)
        if path:
            storage.delete(path)
