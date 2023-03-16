from django.db import models

# Create your models here.
BULLY_CATEGORIES = [
    ('age', 'Age'),
    ('religion', 'Religion'),
    ('gender', 'Gender'),
    ('ethnicityandrace', 'Ethnicity And Race')
]
CATEGORIES = [
    ("notcyberbullying", "Not Cyber bullying"),
    ("cyberbullying", "Cyber Bullying"),
]


class ClassifyCyberBullying(models.Model):
    text = models.TextField()
    text_type = models.CharField(max_length = 500)

    def __str__(self):
        return self.text


class CyberBullyingOrNot(models.Model):
    text = models.TextField()
    text_type = models.CharField(max_length = 255)

    def __str__(self):
        return self.text


class Slang(models.Model):
    slang = models.TextField()
    word = models.CharField(max_length = 255)

    def __str__(self):
        return self.text


class EthnicityAndRaceGlossary(models.Model):
    word = models.CharField(max_length=250)

    def __str__(self):
        return self.word


class AgeGlossary(models.Model):
    word = models.CharField(max_length=250)

    def __str__(self):
        return self.word


class GenderGlossary(models.Model):
    word = models.CharField(max_length=250)

    def __str__(self):
        return self.word


class ReleigionGlossary(models.Model):
    word = models.CharField(max_length=250)

    def __str__(self):
        return self.word


class Negation(models.Model):
    word = models.CharField(max_length=250)

    def __str__(self):
        return self.word
    

class OffensiveWithSeverity(models.Model):
    word = models.CharField(max_length=250)
    severity = models.IntegerField()
    
    def __str__(self):
        return self.word