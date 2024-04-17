# Generated by Django 4.2.7 on 2024-04-17 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('tipo', models.CharField(choices=[('TXT', 'Texto'), ('INT', 'Intervalo'), ('MUL', 'Múltipla Escolha')], max_length=3)),
                ('formulario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.formulario')),
            ],
        ),
        migrations.CreateModel(
            name='Opcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=100)),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.pergunta')),
            ],
        ),
    ]
