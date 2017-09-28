from django.shortcuts import render
from .models import Wojewodztwo, Gmina, Kandydat, Glosy, Karty
from .dane import dane
from django.db.models import Sum
from django.http import *
from .forms import Logowanie
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
import json
from django.db import IntegrityError,transaction



@transaction.atomic
@require_POST
def zalogowany(request):
    try:
        with transaction.atomic():
            if request.user.is_authenticated():
                return HttpResponse("OK")
            else:
                return HttpResponse("NO")
    except IntegrityError:
        return HttpResponse("NO")

@transaction.atomic
@require_GET
def data_edycji(request):
    try:
        with transaction.atomic():
            if("id" in request.GET):
                data = Gmina.objects.get(id=request.GET["id"])
                return HttpResponse(data.czas)
            else:
                return HttpResponseForbidden("Niepoprawne dane!")
    except IntegrityError:
        return HttpResponseForbidden("Problem z bazą danych!")


@transaction.atomic
@login_required
@require_POST
def edytuj(request):

    # Zabezpiecznie przed niepoprawnymi danymi
    if (( "kandydat" not in request.POST) or ( "id" not in request.POST) or ( "mieszkancy" not in request.POST) or
            ("uprawnieni" not in  request.POST) or ("karty" not in request.POST) or ("glosy" not in request.POST)
        or ("wazne" not in request.POST)):
        return HttpResponseForbidden("Niepoprawne dane!")

    kandydat = Kandydat.objects.get(id=request.POST["kandydat"])
    gmina_edycja = Gmina.objects.get(id=request.POST["id"])
    karty_edycja = Karty.objects.get(gmina_id=request.POST["id"])
    glosy_edycja = Glosy.objects.get(gmina_id=request.POST["id"])

    mieszkancy = int(request.POST["mieszkancy"])
    uprawnieni = int(request.POST["uprawnieni"])
    karty = int(request.POST["karty"])
    glosy = int(request.POST["glosy"])
    wazne = int(request.POST["wazne"])

    # Sprawdź poprawność danych
    walidacja = []
    walidacja.append(uprawnieni)
    walidacja.append(karty)
    walidacja.append(wazne)
    walidacja.append(glosy)

    if(mieszkancy<0):
        return HttpResponseForbidden("Niepoprawne dane!")
    poprzedni = mieszkancy

    for i in walidacja:
        print(i)
        if(i < 0):
            return HttpResponseForbidden("Niepoprawne dane!")
        if(poprzedni < i):
            return HttpResponseForbidden("Niepoprawne dane!")
        poprzedni = i

    try:
        with transaction.atomic():
            gmina_edycja.liczba_mieszkancow = mieszkancy
            gmina_edycja.uprawnieni = uprawnieni
            karty_edycja.liczba = karty
            glosy_edycja.glosy_na_wybranego_kanydata = glosy
            glosy_edycja.wazne = wazne
            glosy_edycja.kandydat=kandydat


            gmina_edycja.save()
            karty_edycja.save()
            glosy_edycja.save()

            return HttpResponseRedirect("/")

    except IntegrityError:
        return HttpResponseForbidden("Problem z bazą danych!")


@login_required
@require_GET
def wyloguj(request):
    logout(request)
    return HttpResponseRedirect("/")




def filtr(request):

    if("woj" in request.GET and "rodzaj" in request.GET and "min" in request.GET and "max" in request.GET):
        if request.GET["woj"] != 'dowolne':
            dobre = Gmina.objects.filter(wojewodztwo__nazwa=request.GET["woj"])
        else:
            dobre = Gmina.objects.all()

        if request.GET["rodzaj"] != 'dowolne':
            dobre2 = dobre.filter(rodzaj=request.GET["rodzaj"][0])
        else:
            dobre2 = dobre

        if request.GET["min"] != '':
            dobre3 = dobre2.filter(liczba_mieszkancow__gte= request.GET["min"])
        else:
            dobre3 = dobre2

        if request.GET["max"] != '':
            dobre4 = dobre3.filter(liczba_mieszkancow__lte=request.GET["max"])
        else:
            dobre4 = dobre3

        zbiorcze = {}
        kandydaci = []
        kandydaci.append(Kandydat.objects.all()[0].id)
        kandydaci.append(Kandydat.objects.all()[1].id)
        kandydaci.append(Kandydat.objects.all()[0].nazwisko)
        kandydaci.append(Kandydat.objects.all()[1].nazwisko)
        zbiorcze['kandydaci'] = kandydaci

        for i in dobre4:
            dane=[]
            dane.append(i.id)
            dane.append(i.nazwa)
            dane.append(i.liczba_mieszkancow)
            dane.append(i.uprawnieni)
            dane.append(Karty.objects.get(gmina=i).liczba)
            dane.append(Glosy.objects.get(gmina=i).wazne)
            dane.append(Glosy.objects.get(gmina=i).glosy_na_wybranego_kanydata)
            dane.append(Glosy.objects.get(gmina=i).kandydat.id)
            zbiorcze[i.nazwa]=dane

        return HttpResponse(json.dumps(zbiorcze), content_type='application/json')
    else:
        return HttpResponseForbidden("Niepoprawne dane!")



@require_POST
def loguj(request):
    if("login" in request.POST and "haslo" in request.POST):
        user = authenticate(username=request.POST["login"], password=request.POST["haslo"])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseForbidden("Bad username or password.")
    else:
        return HttpResponseForbidden("Niepoprawne dane")



def main(request):

    # Decyduje kto jest kandydatem, którego potem nazywam
    # pierwszym jako pierwszy w porządku alfabetycznym
    kand1 = Kandydat.objects.all().order_by('imie')[:1].get()
    kand2 = Kandydat.objects.all().order_by('imie')[1:2].get()

    # Wyszukaj wszystkie województwa w bazie danych
    woj = Wojewodztwo.objects.all().order_by('numer')

    # Wyszukaj wszystkie gminy w bazie danych
    gminy = Gmina.objects.all()

    # Wyszukaj wszystkie oddane głosy
    glosy_all = Glosy.objects.all()

    # Policz ile jest w całej Polsce osób uprawnionych do głosowanie:
    # sumuj dane dla każdej gminy w Polsce
    uprawnieni = gminy.aggregate(Sum('uprawnieni'))['uprawnieni__sum']

    # Policz ile jest mieszkańców Polski
    # sumuj dane dla każdej gminy w Polsce
    mieszkancy = Gmina.objects.all().aggregate(Sum('liczba_mieszkancow'))['liczba_mieszkancow__sum']

    # Wyszukaj wszystkie wydane karty
    karty_all = Karty.objects.all()

    # Policz ile wydano kart w całej Polsce
    # sumuj dane dla każdej gminy w Polsce
    karty_wydane =  karty_all.aggregate(Sum('liczba'))['liczba__sum']

    # Policz ile oddano głosów w całej Polsce
    # sumuj dane dla każdej gminy w Polsce
    glosy_suma=  Glosy.objects.all().aggregate(Sum('wazne'))['wazne__sum']

    # Policz ile oddano głosów WAŻNYCH w całej Polsce
    # sumuj dane dla każdej gminy w Polsce
    glosy_wazne =  Glosy.objects.all().aggregate(Sum('wazne'))['wazne__sum']

    # Przekaż dane już obliczone do templates
    zwrot = {'kandydat1': kand1, 'kandydat2': kand2, 'woj': woj, 'uprawnieni': uprawnieni,'karty_wydane': karty_wydane
             ,'glosy_suma':glosy_suma, 'glosy_wazne':  glosy_wazne, 'mieszkancy': mieszkancy}


    # Licz statystyki dla każdego województwa
    # Do template przekazuje słownik lista,
    # w celu pobrania z niego danych dla danego wojewóztwa
    # korzystam z custom tags zdefiniowanych templatetags

    # Zmienne trzymają liczbę głosów z całej Polskie
    kand1_suma = 0
    kand2_suma = 0

    lista ={}

    # Najpierw utworz tablice wszystkich wojewodztw
    for i in woj:
        nowy = dane()
        nowy.nazwa = i.nazwa
        nowy.numer = i.numer
        lista[nowy.nazwa] = nowy

    # Przejrzyj wszystkie głosy
    for i in glosy_all:
            lista[i.gmina.wojewodztwo.nazwa].wazne += i.wazne
            if i.kandydat == kand1:
                # Liczba głosów w danym województwie
                lista[i.gmina.wojewodztwo.nazwa].kandydat_1 += i.glosy_na_wybranego_kanydata
                lista[i.gmina.wojewodztwo.nazwa].kandydat_2 +=i.wazne -i.glosy_na_wybranego_kanydata
                kand1_suma+=i.glosy_na_wybranego_kanydata
                kand2_suma += i.wazne -i.glosy_na_wybranego_kanydata
            else:
                lista[i.gmina.wojewodztwo.nazwa].kandydat_2 += i.glosy_na_wybranego_kanydata
                lista[i.gmina.wojewodztwo.nazwa].kandydat_1 += i.wazne - i.glosy_na_wybranego_kanydata
                kand2_suma += i.glosy_na_wybranego_kanydata
                kand1_suma += i.wazne - i.glosy_na_wybranego_kanydata

    # Przekaż dane już obliczone do templates
    zwrot['lista'] = lista

    # Wynik procentowy kandydatów na całą Polskę
    procentowo_1= (kand1_suma / glosy_wazne) *100
    procentowo_2 = (kand2_suma / glosy_wazne) * 100
    zwrot['kand1_suma'] = kand1_suma
    zwrot['kand2_suma'] = kand2_suma
    zwrot['procentowo_1'] = round(procentowo_1,2)
    zwrot['procentowo_2'] = round(procentowo_2,2)

    request.session.set_expiry(60 * 60)
    if request.method == 'POST':
        form = Logowanie(request.POST)
    else:
        form = Logowanie()

    if request.user.is_authenticated():
        zwrot['zalogowany'] = request.user;
    zwrot['form'] = form

    rodzaj=[]
    for i in Gmina.RODZAJ_ENUM:
        rodzaj.append(i[1])
    zwrot['rodzaj'] = rodzaj
    return render(request, 'PKW/test.html', zwrot)
