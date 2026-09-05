from django.db import models


class Delegacion(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = 'Activa', 'Activa'
        INACTIVA = 'Inactiva', 'Inactiva'

    nombre = models.CharField(max_length=100, unique=True)
    ambito = models.TextField(
        'Ámbito territorial', blank=True,
        help_text='Describe el territorio o área que cubre esta delegación.'
    )
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Delegación'
        verbose_name_plural = 'Delegaciones'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def n_funcionarios(self):
        return self.funcionarios.count()


class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Funcionario(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'Activo', 'Activo'
        INACTIVO = 'Inactivo', 'Inactivo'

    nombre = models.CharField(max_length=150)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name='funcionarios')
    delegacion = models.ForeignKey(Delegacion, on_delete=models.PROTECT, related_name='funcionarios')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)
    es_verificador = models.BooleanField('Es verificador', default=False)

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

    @property
    def iniciales(self):
        partes = self.nombre.split()
        return "".join(p[0] for p in partes[:2]).upper()
