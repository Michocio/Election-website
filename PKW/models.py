from django.db import models
from django.core.validators import MinValueValidator
import datetime

class Wojewodztwo(models.Model):
    numer = models.IntegerField(unique=True, validators = [MinValueValidator(0)])
    nazwa= models.CharField(unique=True, max_length=50)

    def __str__(self):
        # Wyświetlaj nazwe województwa w django admin
        return self.nazwa

    class Meta:
        # Jak djando admin wyświetla liczbę mnogą nazwy modelu
        verbose_name_plural = "wojewodztwa"


class Gmina(models.Model):
    czas =  models.DateTimeField(auto_now=True)
    nazwa = models.CharField(max_length=30)
    RODZAJ_ENUM = (
        ('W', 'Wieś'),
        ('M', 'Miasto'),
        ('Z', 'Zagranica'),
        ('S', 'Statek'),
    )
    rodzaj = models.CharField(max_length=30, choices=RODZAJ_ENUM)
    liczba_mieszkancow = models.IntegerField(validators = [MinValueValidator(0)])
    uprawnieni = models.IntegerField(validators = [MinValueValidator(0)])
    wojewodztwo = models.ForeignKey(Wojewodztwo, on_delete=models.CASCADE)

    def __str__(self):
        # Wyświetlaj nazwe gminy w django admin
        return self.nazwa

    class Meta:
        # Jak djando admin wyświetla liczbę mnogą nazwy modelu
        verbose_name_plural = "gminy"




class Kandydat(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)

    def __str__(self):
        # Wyświetlaj imię i nazwisko kandydata w django admin
        return self.imie +' ' + self.nazwisko

    class Meta:
        # Jak djando admin wyświetla liczbę mnogą nazwy modelu
        verbose_name_plural = "kandydaci"


class Glosy(models.Model):
    #Przyjąłem taki model trzymania danych o głosach na kandydatów:
    # Obiekt dla gminy trzyma info o kandydacie na któego oddano głosy,
    # w liczbie określonej w atrybucie glosy_na_wybranego_kanydata
    # Nie dupilkuje, więc danych - głosy oddane na drogiego kandydata to
    # roznica głosów ważnych i glosy_na_wybranego_kanydata


    wazne = models.IntegerField(validators = [MinValueValidator(0)]) # Liczba WAŻNYCH oddanych głosów w danej gminie
    gmina = models.ForeignKey(Gmina, on_delete=models.CASCADE)

    # Na kogo oddane głosy
    kandydat = models.ForeignKey(Kandydat, on_delete=models.CASCADE, default= 0)
    # Liczba WAŻNYCH oddanych głosów w danej gminie na kandydata określonego linijke wyżej
    glosy_na_wybranego_kanydata = models.IntegerField(validators = [MinValueValidator(0)])

    def __str__(self):
        # Wyświetlaj info o głosach w ładnej formie w django admin
        return "%s %s %s" % (self.kandydat.nazwisko, self.glosy_na_wybranego_kanydata, self.gmina)

    class Meta:
        # Jak djando admin wyświetla liczbę mnogą nazwy modelu
        verbose_name_plural = "glosy"

class Karty(models.Model):
    liczba = models.IntegerField(validators = [MinValueValidator(0)])
    gmina = models.ForeignKey(Gmina, on_delete=models.CASCADE)

    def __str__(self):
        # Wyświetlaj info o wydanych kartach w ładnej formie w django admin
        return "%s %s" % ( self.gmina, self. liczba)

    class Meta:
        # Jak djando admin wyświetla liczbę mnogą nazwy modelu
        verbose_name_plural = "karty"