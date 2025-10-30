# core/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class ActiveQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(is_active=True)

    def soft_delete(self, user=None):
        """Soft delete masivo sobre el queryset."""
        return self.update(is_active=False, deleted_at=timezone.now())

    def restore(self):
        """Restauración masiva."""
        return self.update(is_active=True, deleted_at=None)

class ActiveManager(models.Manager):
    """Manager por defecto: sólo objetos activos."""
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db).alive()

class AllObjectsManager(models.Manager):
    """Manager alternativo: incluye activos e inactivos."""
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)

class SoftDeleteModel(models.Model):
    """
    Mixin abstracto para borrado lógico.
    - is_active: visible/consultable en la API
    - deleted_at: marca de tiempo de baja
    - deleted_by: quién dio de baja (opcional)
    """
    is_active  = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="deleted_%(class)ss"
    )

    # Managers
    objects     = ActiveManager()      # por defecto, sólo vivos
    all_objects = AllObjectsManager()  # incluye todo

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, user=None):
        """Soft delete (no elimina físicamente)."""
        if self.is_active:
            self.is_active = False
            self.deleted_at = timezone.now()
            if user and not self.deleted_by_id:
                self.deleted_by = user
            self.save(update_fields=["is_active", "deleted_at", "deleted_by"])

    def hard_delete(self, using=None, keep_parents=False):
        """Eliminación física (evitar salvo casos especiales)."""
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Reactivar el registro."""
        self.is_active = True
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["is_active", "deleted_at", "deleted_by"])
