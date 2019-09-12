from django.db import models


class MaterialCategory(models.Model):
    name = models.CharField(
        verbose_name='название категории',
        max_length=45,
        unique=True
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True,
        null=True
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='updated'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class MaterialUnits(models.Model):
    name = models.CharField(
        verbose_name='единица измерения',
        max_length=45,
        unique=True
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True,
        null=True
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='updated'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'единица'
        verbose_name_plural = 'единицы'


class Material(models.Model):

    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        verbose_name='категория'
    )

    name = models.CharField(
        verbose_name='материал',
        max_length=128
    )

    short_desc = models.TextField(
        verbose_name='краткое описание',
        max_length=160,
        blank=True,
        null=True
    )

    detail = models.TextField(
        verbose_name='описание',
        blank=True,
        null=True
    )

    count = models.PositiveIntegerField(
        verbose_name='текущее количество',
        default=0
    )

    count_full = models.PositiveIntegerField(
        verbose_name='минимальное количество',
        default=100
    )

    units = models.ForeignKey(
        MaterialUnits,
        on_delete=models.CASCADE,
        verbose_name='единица измерения'
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='updated'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created'
    )

    # @property
    # def count_instance(self):
    #     count_instance = MaterialInstance.objects.filter(material__pk=self.pk).count()
    #     self.count = count_instance
    #     return self.count

    def __str__(self):
        return f'Материал: {self.name}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'


class MaterialInstance(models.Model):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name='Название материала'
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='updated'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created'
    )

    def __str__(self):
        return self.material.name

    class Meta:
        verbose_name = 'Экземляр материала'
        verbose_name_plural = 'Экземляры материала'


class MaterialInstanceHistory(models.Model):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name='Название материала'
    )

    count_deleted = models.IntegerField(
        verbose_name='количество списанных'
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='updated'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created'
    )

    def __str__(self):
        return self.material.name

    class Meta:
        verbose_name = 'Запись удаления'
        verbose_name_plural = 'Записи удаления'
