""" W pliku znajdują się klasy "łącznikowe" między
MODELAMI, a metodami ich wprowadzania przez moduł admin.
W pliku rejestruję modele, tak, żeby admin o nich wiedział
i pozwalał na wprowadzanie danych z poziomu admina."""
from django.contrib import admin
from .models import Wojewodztwo, Gmina, Kandydat, Glosy, Karty
from django.contrib import messages
from django.db.models import Sum

# Zarejestruj model wojewodztwo
admin.site.register(Wojewodztwo)

# Zarejestruj model gmina
@admin.register(Gmina)
class gminaAdmin(admin.ModelAdmin):
    # Sprawdź poprawność wprowadzanych danych dla gmin
    # mieszkańców >= uprawnionych

    # Override metode odpowiadającą za zapisywanie nowej instancji modely
    def save_model(self, request, obj, form, change):
        if  obj.liczba_mieszkancow >= obj.uprawnieni:
            super(gminaAdmin, self).save_model(request, obj, form, change)
        else:
            # Nie wyświetlaj standardowego komunikatu django admin
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Nie może być więcej uprawnionych niż liczba mieszkańców!")


# Zarejestruj model karty
@admin.register(Karty)
class kartyAdmin(admin.ModelAdmin):
    # Sprawdzanie poprawności liczby oddanych kart
    # uprawnionych >= wydanych

    # Override metode odpowiadającą za zapisywanie nowej instancji modely
    def save_model(self, request, obj, form, change):
        # Sprawdź czy istneją już dane wprowadzone dla danej gminy
        istnieje = Karty.objects.filter( gmina=obj.gmina)

        if (change == False and istnieje.count()==0) or change ==True:
            # Jeżeli user próbuje dodać nowe dane dla gminy,
            # która nie ma jeszcze wprowadzonych danych
            # lub próbuje zmienić dane
            uprawnieni = Gmina.objects.filter(id=obj.gmina.id)[0].uprawnieni
            # uprawnionych >= wydanych
            if obj.liczba <= uprawnieni:
                super(kartyAdmin, self).save_model(request, obj, form, change)
            else:
                # Nie wyświetlaj standardowego komunikatu django admin
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Nie możesz wydać więcej kart niż uprawnionych osób w danej gminie!")
        else:
            # User próbuje dodać dane dla gminy, która ma już dodane dane
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Nie możesz dodać danych dla danej gminy dwa razy!")



# Zarejestruj model glosy
@admin.register(Glosy)
class glosyAdmin(admin.ModelAdmin):
    # Sprawdzanie poprawności danych dotyczących oddanych głosów
    # wydanych >= oddanych
    # oddanych >= ważnych

    # Override metode odpowiadającą za zapisywanie nowej instancji modely
    def save_model(self, request, obj, form, change):
        suma_wydanych = Karty.objects.filter(gmina=obj.gmina)[0].liczba

        # Ochrona przed ponownym dodaniem glosow dla danej gminy
        wyniki_dla_gminy = Glosy.objects.filter(gmina = obj.gmina).count()

        # Jeżeli user próbuje dodać nowe dane dla gminy,
        # która nie ma jeszcze wprowadzonych danych
        # lub próbuje zmienić dane
        if (change == False and wyniki_dla_gminy == 0) or change == True :
            if suma_wydanych >= obj.wazne and obj.wazne>=obj.glosy_na_wybranego_kanydata:
                # wydanych >= oddanych
                # oddanych >= ważnych
                super(glosyAdmin, self).save_model(request, obj, form, change)
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Nie możesz oddać więcej głosów niż liczba wydanych kart!")
        else:
            # User próbuje dodać dane dla gminy, która ma już dodane głosy
             messages.set_level(request, messages.ERROR)
             messages.error(request, "Nie możesz dodać głosów po raz drugi dla tej samej gminy!")



@admin.register(Kandydat)
class kandydatAdmin(admin.ModelAdmin):
# Zapobieganie dodaniu więcej niż dwóćh kandydatów

    def save_model(self, request, obj, form, change):
        if  (change == True) or (Kandydat.objects.count() < 2):
            super(kandydatAdmin, self).save_model(request, obj, form, change)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Nie możesz dodać więcej niż dwóch kandydatów!")