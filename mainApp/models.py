from django.db import models
from datetime import date

#
class regions(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, verbose_name="Назва району", help_text="")
    director = models.CharField(max_length=100, null=False, default='', verbose_name="Начальник району", help_text="")
    telephone = models.CharField(max_length=30, null=False, default='', verbose_name="№ телефону ч/ч", help_text="")

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'db_regions'


class category(models.Model):
    name = models.CharField(max_length=255, null=False, default='', verbose_name="Тип об`єкту")

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'db_category'


class firms(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, default='', db_index=True, verbose_name="Назва")
    director = models.CharField(max_length=100, null=False, blank=False, default='', verbose_name="Начальник")
    yur_address = models.CharField(max_length=255, null=False, blank=False, default='', verbose_name="Юр. адреса")
    fiz_address = models.CharField(max_length=255, verbose_name="Фіз. адреса")
    telephone1 = models.CharField(max_length=30, null=False, default='', verbose_name="№ телефону")
    telephone2 = models.CharField(max_length=30, blank=True, verbose_name="№ телефону (дод)")
    
    def __str__(self):
        return self.name

    class Meta():
        db_table = 'db_firm'


class security_object(models.Model):
    CHOICES = (
        ('kv', 'Квартира (ОМГ)'),
        ('in', 'Інше')
    )
    firm = models.ForeignKey('firms', on_delete=models.CASCADE, verbose_name="Ох. фірма")
    dogovor = models.ForeignKey('dogovor', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Договір")
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, default='', db_index=True, verbose_name="Назва")
    address = models.CharField(max_length=255, null=False, blank=False, default='', verbose_name="Адреса")
    region = models.ForeignKey('regions', null=True, on_delete=models.SET_NULL, verbose_name="Район")
    document = models.FileField(upload_to='object', verbose_name="Картка об`єкту")
    state = models.CharField(max_length=2, choices=CHOICES, null=False, blank=False, default='', verbose_name="Тип")
    category = models.ForeignKey('category', null=True, on_delete=models.SET_NULL, verbose_name="Категорія")

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'db_security_object'


class dogovor(models.Model):
    CHOICES = (
        ('new', 'Новий'),
        ('per', 'Перезаключений'),
        ('pro', 'Пролонгований'),
        ('fin', 'Розірваний')
    )
    firm = models.ForeignKey('firms', on_delete=models.CASCADE, verbose_name="Ох. фірма")
    name = models.CharField(max_length=50, verbose_name="№ договору")
    dogovor_file = models.FileField(upload_to='dogovor', verbose_name="Скан договору")
    date_start = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False, default=date.today, verbose_name="Дата поч.")
    date_finish = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name="Дата зак.")
    state = models.CharField(max_length=3, choices=CHOICES, null=False, blank=False, default='new', verbose_name="Тип",
                             help_text="")

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'db_dogovor'
