from django.test import TestCase
from .models import Kandydat, Gmina, Glosy, Karty, Wojewodztwo
import datetime
from django.contrib.auth.models import User

# Create your tests here.
class testy_ajax(TestCase):

    def setUp(self):

        user = User.objects.create_user('michocio', 'm@m.pl', 'pass12345')
        Wojewodztwo(numer=1,nazwa='mazowieckie').save()
        maz = Wojewodztwo.objects.get(numer=1)
        Wojewodztwo(numer=2, nazwa='lubelskie').save()
        lubl = Wojewodztwo.objects.get(numer=2)
        Wojewodztwo(numer=3, nazwa='lubuskie').save()
        lub = Wojewodztwo.objects.get(numer=3)
        Wojewodztwo(numer=4, nazwa='podkarpackie').save()
        pod = Wojewodztwo.objects.get(numer=4)

        Gmina(czas=datetime.datetime.now(),nazwa='warszawa',rodzaj='M',liczba_mieszkancow=1500000
              ,uprawnieni=1200000,wojewodztwo=maz).save()
        warszawa = Gmina.objects.get(nazwa='warszawa')
        Gmina(czas=datetime.datetime.now(), nazwa='lublin', rodzaj='M', liczba_mieszkancow=150000,
              uprawnieni=120000, wojewodztwo=lubl).save()
        lublin = Gmina.objects.get(nazwa='lublin')
        Gmina(czas=datetime.datetime.now(), nazwa='zamość', rodzaj='W', liczba_mieszkancow=10000,
              uprawnieni=9999, wojewodztwo=lubl).save()
        zamosc  = Gmina.objects.get(nazwa='zamość')
        Gmina(czas=datetime.datetime.now(), nazwa='lubin', rodzaj='M', liczba_mieszkancow=3500000,
              uprawnieni=2200000, wojewodztwo=lub).save()
        lubin = Gmina.objects.get(nazwa='lubin')
        Gmina(czas=datetime.datetime.now(), nazwa='marki', rodzaj='W', liczba_mieszkancow=900000,
              uprawnieni=800000, wojewodztwo=maz).save()
        marki = Gmina.objects.get(nazwa='marki')
        Gmina(czas=datetime.datetime.now(), nazwa='rzeszów', rodzaj='M', liczba_mieszkancow=700000,
              uprawnieni=600000, wojewodztwo=pod).save()
        rzaszow = Gmina.objects.get(nazwa='rzeszów')
        Gmina(czas=datetime.datetime.now(), nazwa='krosno', rodzaj='M', liczba_mieszkancow=2,
              uprawnieni=1, wojewodztwo=pod).save()
        krosno = Gmina.objects.get(nazwa='krosno')
        Gmina(czas=datetime.datetime.now(), nazwa='piaseczno', rodzaj='M', liczba_mieszkancow=3500000,
              uprawnieni=2200000, wojewodztwo=maz).save()
        piaseczno = Gmina.objects.get(nazwa='piaseczno')

        Kandydat(imie="jan", nazwisko="kowalski").save()
        kand1=Kandydat.objects.get(imie="jan")
        Kandydat(imie="ania", nazwisko="maj").save()
        kand2 = Kandydat.objects.get(imie="ania")

        Karty(liczba=1000000, gmina=warszawa).save()
        Karty(liczba=100000, gmina=lublin).save()
        Karty(liczba=8000, gmina=zamosc).save()
        Karty(liczba=2000000, gmina=lubin).save()
        Karty(liczba=50000, gmina=marki).save()
        Karty(liczba=50000, gmina=rzaszow).save()
        Karty(liczba=0, gmina=krosno).save()
        Karty(liczba=1500000, gmina=piaseczno).save()


        Glosy(wazne=700000, gmina=warszawa,kandydat=kand1, glosy_na_wybranego_kanydata=350000).save()
        Glosy(wazne=300000, gmina=lublin,kandydat=kand2, glosy_na_wybranego_kanydata=100000).save()
        Glosy(wazne=5000, gmina=zamosc,kandydat=kand2, glosy_na_wybranego_kanydata=3).save()
        Glosy(wazne=1000000, gmina=lubin,kandydat=kand1, glosy_na_wybranego_kanydata=700000).save()
        Glosy(wazne=44000, gmina=marki,kandydat=kand2, glosy_na_wybranego_kanydata=34000).save()
        Glosy(wazne=40000, gmina=rzaszow,kandydat=kand1, glosy_na_wybranego_kanydata=10000).save()
        Glosy(wazne=0, gmina=krosno,kandydat=kand2, glosy_na_wybranego_kanydata=0).save()
        Glosy(wazne=1000000, gmina=piaseczno,kandydat=kand1, glosy_na_wybranego_kanydata=500000).save()
        count = Karty.objects.count()
        self.assertEqual(count, 8)

    def test_gminy_zapytanie_dowolne(self):
        response = self.client.get('/filtr/?woj=dowolne&rodzaj=dowolne&min=&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 9)
        self.assertTrue("warszawa" in zwrot)
        self.assertTrue("lublin" in zwrot)
        self.assertTrue("lubin" in zwrot)
        self.assertTrue("krosno" in zwrot)
        self.assertTrue("paryz" not in zwrot)
        self.assertTrue("zamość" in zwrot)
        self.assertTrue("marki" in zwrot)
        self.assertTrue("piaseczno" in zwrot)
        self.assertTrue("rzeszów" in zwrot)

    def test_gminy_zapytanie_wojewodztwo(self):
        response = self.client.get('/filtr/?woj=mazowieckie&rodzaj=dowolne&min=&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 4)
        self.assertTrue("zamość" not in zwrot)
        self.assertTrue("warszawa" in zwrot)
        self.assertTrue("marki" in zwrot)
        self.assertTrue("piaseczno" in zwrot)

        response = self.client.get('/filtr/?woj=lubuskie&rodzaj=dowolne&min=&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 2)
        self.assertTrue("lublin" not in zwrot)
        self.assertTrue("lubin" in zwrot)

        response = self.client.get('/filtr/?woj=lubuskiex&rodzaj=dowolne&min=&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 1)

    def test_gminy_zapytanie_rodzaj(self):
        response = self.client.get('/filtr/?woj=dowolne&rodzaj=Miasto&min=&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 7)
        self.assertTrue("zamość" not in zwrot)
        self.assertTrue("warszawa" in zwrot)
        self.assertTrue("marki" not in zwrot)
        self.assertTrue("piaseczno" in zwrot)

        response = self.client.get('/filtr/?woj=dowolne&rodzaj=Wieś&min=&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 3)
        self.assertTrue("zamość"  in zwrot)
        self.assertTrue("warszawa" not in zwrot)
        self.assertTrue("marki"  in zwrot)
        self.assertTrue("piaseczno" not in zwrot)


    def test_gminy_zapytanie_min(self):
        response = self.client.get('/filtr/?woj=dowolne&rodzaj=dowolne&min=3&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot),8)
        self.assertTrue("krosno" not in zwrot)
        self.assertTrue("warszawa" in zwrot)
        self.assertTrue("marki" in zwrot)
        self.assertTrue("piaseczno" in zwrot)

        response = self.client.get('/filtr/?woj=dowolne&rodzaj=dowolne&min=3500000&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 3)
        self.assertTrue("krosno" not in zwrot)
        self.assertTrue("warszawa" not in zwrot)
        self.assertTrue("lubin" in zwrot)
        self.assertTrue("piaseczno" in zwrot)

    def test_gminy_zapytanie_max(self):
        response = self.client.get('/filtr/?woj=dowolne&rodzaj=dowolne&min=&max=3', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 2)
        self.assertTrue("krosno"  in zwrot)
        self.assertTrue("warszawa" not  in zwrot)
        self.assertTrue("marki" not in zwrot)
        self.assertTrue("piaseczno" not in zwrot)

        response = self.client.get('/filtr/?woj=dowolne&rodzaj=dowolne&min=&max=1500000', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 7)
        self.assertTrue("warszawa"  in zwrot)
        self.assertTrue("piaseczno"not  in zwrot)

    def test_gminy_zapytanie_rozne_1(self):
        response = self.client.get('/filtr/?woj=mazowieckie&rodzaj=Wieś&min=3&max=', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 2)
        self.assertTrue("warszawa" not in zwrot)
        self.assertTrue("marki"  in zwrot)
        self.assertTrue("piaseczno" not in zwrot)

        response = self.client.get('/filtr/?woj=mazowieckie&rodzaj=Wieś&min=&max=800000', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 1)

    def test_gminy_zapytanie_rozne_2(self):
        response = self.client.get('/filtr/?woj=dowolne&rodzaj=Statek&min=3&max=4', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 1)


    def test_gminy_zapytanie_rozne_3(self):
        response = self.client.get('/filtr/?woj=mazowieckie&rodzaj=Miasto&min=1500000&max=1500000', follow=True)
        zwrot = dict(response.json())
        self.assertEqual(len(zwrot), 2)


    def test_edycja_danych(self):
        id = Gmina.objects.get(nazwa='lublin').id
        kand= Kandydat.objects.get(imie="jan")
        self.client.login(username='michocio', password='pass12345')
        response = self.client.post('/edytuj/', {'id':id, 'mieszkancy':7, 'uprawnieni' :6,'karty':5, 'wazne':4, 'glosy':4, 'kandydat':kand.id})
        gmina = Gmina.objects.get(nazwa='lublin')
        self.assertEqual(gmina.liczba_mieszkancow,7);
        self.assertEqual(gmina.uprawnieni, 6);
        karty=Karty.objects.get(gmina_id=id)
        self.assertEqual(karty.liczba, 5);
        glosy=Glosy.objects.get(gmina_id=id)
        self.assertEqual(glosy.wazne, 4);
        self.assertEqual(glosy.glosy_na_wybranego_kanydata, 4);
        self.assertEqual(glosy.kandydat, kand);

        response = self.client.post('/edytuj/',
                                    {'id': id, 'mieszkancy': 777, 'uprawnieni': 777, 'karty': 777, 'wazne': 777, 'glosy': 777,
                                     'kandydat': kand.id})
        gmina = Gmina.objects.get(nazwa='lublin')
        self.assertEqual(gmina.liczba_mieszkancow, 777);
        self.assertEqual(gmina.uprawnieni, 777);
        karty = Karty.objects.get(gmina_id=id)
        self.assertEqual(karty.liczba, 777);
        glosy = Glosy.objects.get(gmina_id=id)
        self.assertEqual(glosy.wazne, 777);
        self.assertEqual(glosy.glosy_na_wybranego_kanydata, 777);
        self.assertEqual(glosy.kandydat, kand);

    def test_czas_edycja(self):
        lublin = Gmina.objects.get(nazwa='lublin')
        self.client.login(username='michocio', password='pass12345')
        response = self.client.get('/data_edycja/?id='+str(lublin.id), follow=True)
        czas = str(Gmina.objects.get(nazwa='lublin').czas)
        self.assertEqual(response.content.decode("utf-8"), czas)