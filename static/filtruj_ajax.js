function filtruj_dane(zalogowany) {

    window.scrollTo(0, 0);
    var woj = document.getElementById("wojewodztwo").value;
    var rodzaj = document.getElementById("gmina").value;
    var min = document.getElementById("min").value;
    var max = document.getElementById("max").value;


    $('.tlo_okno').show();
    $('#edycja_danych').show();

    var filtr = new XMLHttpRequest();
    filtr.addEventListener("abort", function() {
        alert("Błąd przy ładowaniu wyników");
        return;
    });

     filtr.addEventListener("error", function() {
        alert("Błąd przy ładowaniu wyników");
        return;
    });


    filtr.addEventListener("load", function() {

            var obj = JSON.parse(this.responseText);
            var tab = document.createElement("table");
            $('#edycja_danych').append(tab);
            var rzad=0;

            var kand1 = obj['kandydaci'][2];
            var kand2 = obj['kandydaci'][3];
            var kand1_id = obj['kandydaci'][0];
            var kand2_id = obj['kandydaci'][1];


            for(i in obj)
            {
                if(i!='kandydaci') {
                    if (!(rzad % 2 ))
                        var kolor = '#dedcd0';
                    else
                        var kolor = '#9AA6B8';

                    var tr = document.createElement("tr");
                    var ktory = 0;
                    for (j in obj[i]) {
                        if (ktory > 1 && ktory!=7) {
                            var input = document.createElement("input");
                            input.type = "text";
                            input.value = obj[i][j];
                            input.style.backgroundColor = 'inherit';
                            input.onkeypress =
                               function(event)
                               {
                                  return event.charCode >= 48 && event.charCode <= 57;
                               };
                            input.addEventListener("change", function () {
                                      this.style.backgroundColor = "crimson";
                                    });
                            input.style.borderStyle = 'solid';
                            input.style.borderWidth = '0';
                            input.style.cursor = 'pointer';
                            input.style.textAlign='center';
                            if(zalogowany==0) {
                                input.readOnly = true;
                                input.style.cursor = 'default';
                            }
                            tr.appendChild(document.createElement("td")).appendChild(input);
                        }
                        else if (ktory == 1) {
                            var nazwa =  obj[i][j].charAt(0).toUpperCase() + obj[i][j].slice(1);
                            tr.appendChild(document.createElement("td")).appendChild(document.createTextNode(nazwa));
                        }
                        ktory++;
                    }
                    if(zalogowany==1) {
                        var select = document.createElement("select");

                        var opt1 = document.createElement("option");
                        var opt2 = document.createElement("option");

                        opt1.innerHTML = kand1;
                        opt1.value = kand1_id;

                        opt2.innerHTML = kand2;
                        opt2.value = kand2_id;

                        select.appendChild(opt1);
                        select.appendChild(opt2);

                        if (kand1_id == obj[i][7])
                            opt1.selected = "selected";
                        else
                            opt2.selected = "selected";

                        tr.appendChild(document.createElement("td")).appendChild(select);
                    }
                    else
                    {
                        var nazwa;
                        if (kand1_id == obj[i][7])
                            nazwa =  kand1;
                        else
                            nazwa =  kand2;
                        tr.appendChild(document.createElement("td")).appendChild(document.createTextNode(nazwa));
                    }
                    if(zalogowany==1) {
                        var button = document.createElement("button");
                        button.innerHTML = "Zmien";

                        tr.id = "tr" + obj[i][0];
                        button.id = obj[i][0];
                        button.setAttribute('onclick', 'edytuj_dane(this.id)');

                        tr.appendChild(button);
                    }
                    document.getElementById("tbl").appendChild(tr);

                    rzad++;
                }
            }

    });
    filtr.open("GET", "filtr/?woj=" + woj + "&rodzaj=" + rodzaj + "&min=" + min + "&max=" + max, true);
    filtr.send();

}

function wyloguj()
{
    var rob = new XMLHttpRequest();
    rob.open("GET", "wyloguj/", true);
    rob.send();
    window.location.reload();
}