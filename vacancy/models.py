from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from company.models import Company

class Vacancy(models.Model):
    status = models.BooleanField(default=True)
    completed_by_here = models.BooleanField(default=False, blank=True, verbose_name="Essa vaga foi preenchida por aqui?")

    #INFORMAÇÕES BASICAS
    ocupacao = models.CharField(max_length=255, verbose_name="Ocupação")

    tipo_choice = [
        ('0', 'CLT'),
        ('1', 'Contrato'),
        ('2', 'Estágio'),
    ]

    tipo_vaga = models.CharField(
        max_length=2,
        choices=tipo_choice,
        verbose_name="Tipo da vaga"
    )

    descricao_atividade = models.TextField(max_length=255, verbose_name="Atividades a serem desenvolvidas")

    observacoes = models.TextField(blank=True, max_length=255, verbose_name="Observações sobre a vaga")

    local_trabalho = models.CharField(max_length=255, verbose_name="Local de trabalho")

    local_entrevista = models.CharField(max_length=255, verbose_name="Local da entrevista")

    quantidade_vagas = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

    jornada_trabalho = models.IntegerField(
        default=4,
        validators=[
            MaxValueValidator(24),
            MinValueValidator(4)
        ],
        verbose_name="Jornada de trabalho"
    )

    #REQUISITOS
    exp_choices = [
        ("0", "CTPS"),
        ("1", "Contrato"),
        ("2", "Declaração"),
    ]

    experiencia_comprovada = models.CharField(
        blank=True,
        max_length=2,
        verbose_name="Experiencia Comprovada",
        choices=exp_choices
    )

    tempo_experiencia = models.IntegerField(
        blank=True,
        default=1,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ],
        verbose_name="Tempo de Experiência"
    )

    tipo_tempo_choices=[
        ("0", "meses"),
        ("1", "anos"),
    ]

    tipo_tempo = models.CharField(
        blank=True,
        default="",
        max_length=2,
        choices=tipo_tempo_choices,
    )

    escolaridade_choice = [
        ('0', 'Ensino fundamental completo'),
        ('1', 'Ensino médio completo'),
        ('2', 'Cursando ensino médio'),
        ('3', 'Cursando superior'),
        ('4', 'Superior completo'),
        ('5', 'Cursando técnico'),
        ('6', 'Técnico completo'),
    ]

    escolaridade = models.CharField(
        max_length=2,
        default="",
        choices=escolaridade_choice,
    )

    curso = models.CharField(
        max_length=30,
        verbose_name="Curso",
        blank=True,
    )

    semestre = models.IntegerField(
        verbose_name="Semestre",
        blank=True,
        default=1,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ],
    )

    chn_choice = [
        ('0', 'CATEGORIA A'),
        ('1', 'CATEGORIA B'),
        ('2', 'CATEGORIA C'),
        ('3', 'CATEGORIA D'),
        ('4', 'CATEGORIA E'),
    ]

    cnh = models.CharField(
        blank=True,
        default="",
        max_length=2,
        choices=chn_choice
    )

    language_select = [
        ('0', 'Inglês'),
        ('1', 'Espanhol'),
        ('2', 'Francês'),
        ('3', 'Chinês'),
        ('4', 'Alemão'),
    ]

    nivel_language = [
        ('0', 'Básico'),
        ('1', 'Intermédiario'),
        ('2', 'Avançado'),
        ('3', 'Fluente'),
    ]

    language = models.CharField(
        blank=True,
        max_length=2,
        choices=language_select,
        default="",
        verbose_name="Idioma"
    )

    nivel = models.CharField(
        blank=True,
        max_length=2,
        choices=nivel_language,
        default="",
        verbose_name="Nível"
    )

    perfil_comportamental_choice = [
        ('0', 'Comunicador'),
        ('1', 'Planejador'),
        ('2', 'Executor'),
        ('3', 'Analista'),
    ]

    perfil_comportamental = models.CharField(
        max_length=2,
        default="",
        choices=perfil_comportamental_choice,
    )

    # PCD
    pcd_auditiva = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Auditiva",
    )
    pcd_mental = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Mental"
    )
    pcd_nanismo = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Nanismo"
    )
    pcd_visao = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Visual"
    )
    pcd_membros_superiores = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Física: Membros superiores"
    )
    pcd_membros_inferiores = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Física: Membros inferiores"
    )

    # BENEFICIOS
    salario_fixo = models.IntegerField(
        verbose_name="Salário fixo",
        default=400,
        validators=[
            MaxValueValidator(10000),
            MinValueValidator(400)
        ],
    )
    comissao = models.BooleanField(
        verbose_name="Comissão",
        default=False
    )

    percentual = models.IntegerField(
            verbose_name="Percentual",
        blank=True,
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
    )

    transporte = models.BooleanField(default=False, verbose_name="Transporte")
    refeicao = models.BooleanField(default=False, verbose_name="refeição")
    transporte_empresa = models.BooleanField(default=False, verbose_name="Transporte da empresa")
    refeitorio_empresa = models.BooleanField(default=False, verbose_name="Refeitório da empresa")
    ass_medica = models.BooleanField(default=False, verbose_name="Assistência médica")
    ass_odonto = models.BooleanField(default=False, verbose_name="Assistência odontológica")
    seguro_vida = models.BooleanField(default=False, verbose_name="Seguro de vida")
    add_noturno = models.BooleanField(default=False, verbose_name="Adicional noturno")
    cesta_basica = models.BooleanField(default=False, verbose_name="Cesta básica")
    add_periculosidade = models.BooleanField(default=False, verbose_name="Adicional periculosidade")
    uniforme = models.BooleanField(default=False, verbose_name="Uniforme")
    auxilio_creche = models.BooleanField(default=False, verbose_name="Auxílio creche")

    # DETALHES DA VAGA
    exp_imprescindivel = models.TextField(
        max_length=255,
        blank=True,
        verbose_name="Experiência ou fator imprescindível"
    )

    exp_desejavel = models.TextField(
        max_length=255,
        blank=True,
        verbose_name="Experiência ou fator desejável"
    )

    extra_info = models.TextField(
        max_length=255,
        blank=True,
        verbose_name="Informações adicionais sobre a vaga"
    )

    data_entrevista = models.DateTimeField(verbose_name="Data da entrevista")

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(self.ocupacao, self.company)