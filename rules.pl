%Hechos
%rango_temperatura
%humedad
%velocidad_viento
%clouds_pct
%lloviendo
%nevando

frio(X) :- rango_temperatura(X, _, Max), Max =< 10.
templado(X) :- rango_temperatura(X, Min, Max), Min > 10, Max =< 30.
caliente(X) :- not(frio(X)), not(templado(X)).

volatil(X) :- rango_temperatura(X, Min, Max), Min \== Max.
estable(X) :- rango_temperatura(X, Min, Max), Min == Max.

humedo(X) :- humedad(X, Pct), Pct >= 50.
seco(X) :- humedad(X, Pct), Pct < 50.

ventisca(X) :- velocidad_viento(X, Velocidad), Velocidad >= 10.
sofocante(X) :- velocidad_viento(X, Velocidad), Velocidad < 10.

nublado(X) :- clouds_pct(X, Pct), Pct >= 50.
despejado(X) :- clouds_pct(X, Pct), Pct < 50.
