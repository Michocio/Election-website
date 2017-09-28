
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function edytuj_dane(id) {
    var edytuj = new XMLHttpRequest();
    edytuj.open("POST", "edytuj/", true);

    var csrftoken = getCookie('csrftoken');
    edytuj.setRequestHeader("X-CSRFToken", csrftoken);
    edytuj.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    //Liczba uprawnionych	Liczba wydanych kart	Liczba głosów ważnych	Głosów na kandydata	Kanydat
    var tr ="tr" + id;
    var mieszkancy = document.getElementById(tr);

    var liczby=[];
    var iterator = mieszkancy.firstElementChild.nextElementSibling;
    var stop= true;
    for(var i=0;i<=5;i++)
    {
        liczby[i]= Number(iterator.firstElementChild.value);
        iterator=iterator.nextElementSibling;
        if(i!=0 && i!=5) {
            if (liczby[i - 1] < liczby[i]) {
                stop = false;
                break;
            }
        }
    }
   var zalogowany = true;
    var czy_zalogowany = new XMLHttpRequest();
    czy_zalogowany.open("POST", "zalogowany/", false);
    czy_zalogowany.setRequestHeader("X-CSRFToken", csrftoken);
    czy_zalogowany.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    czy_zalogowany.send();
    //czy_zalogowany.addEventListener("load", function() {
        if(czy_zalogowany.responseText=="NO"){
            alert("Zaloguj się żeby edytować wyniki!");
            zalogowany=false;
        }
   //});

    if(stop==true && zalogowany==true) {
        var pytaj = new XMLHttpRequest();
        pytaj.open("GET", "data_edycja/?id=" + id, true);
        pytaj.send();
        pytaj.addEventListener("load", function() {
             if(confirm("Wyniki wybranej gminy były ostanio edytowane:\n" + this.responseText +
                 "\nCzy na pewno chcesz dokonać edycji?"))
                edytuj.send("id=" + id + "&mieszkancy=" + liczby[0] + "&uprawnieni=" + liczby[1] +
                    "&karty=" + liczby[2] + "&wazne=" + liczby[3] + "&glosy=" + liczby[4] + "&kandydat=" + liczby[5]);
        });
            pytaj.addEventListener("abort", function() {
            alert("Błąd przy ładowaniu daty ostatniej odpowiedzi");
            return;
        });

         pytaj.addEventListener("error", function() {
            alert("Błąd przy ładowaniu daty ostatniej odpowiedzi");
            return;
        });
    }
    else if(zalogowany==true)
        alert("Dane wprowadzone nieprawidłowo!");
}

function ostatnia_edycja(id) {
    var pytaj = new XMLHttpRequest();
    pytaj.open("GET", "data_edycja/?id=" + id, true);
    pytaj.send();
    pytaj.addEventListener("load", function() {
        return this.responseText.toString();
    });
    pytaj.addEventListener("abort", function() {
        alert("Błąd przy ładowaniu daty ostatniej odpowiedzi");
        return;
    });

     pytaj.addEventListener("error", function() {
        alert("Błąd przy ładowaniu daty ostatniej odpowiedzi");
        return;
    });

}