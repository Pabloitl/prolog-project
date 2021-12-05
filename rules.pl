%%%%%%%%%%%%%%%%%%
% Hechos         %
%%%%%%%%%%%%%%%%%%

%rango_temperatura(x, min, max)
%humedad(x, pct)
%velocidad_viento(x, vel)
%clouds(x, pct)
%lloviendo(x)
%nevando(x)
%soleado(X)

%%%%%%%%%%%%%%%%%%
% Reglas         %
%%%%%%%%%%%%%%%%%%

gelido(X)    :- rango_temperatura(X, _, Max), Max =< -30.
frio(X)      :- rango_temperatura(X, _, Max), Max =< 10.
templado(X)  :- rango_temperatura(X, Min, Max), Min > 10, Max =< 30.
caliente(X)  :- rango_temperatura(X, Min, _), Min > 30.

volatil(X)   :- rango_temperatura(X, Min, Max), Min \== Max.
estable(X)   :- rango_temperatura(X, Min, Max), Min == Max.

humedo(X)    :- humedad(X, Pct), Pct >= 50.
seco(X)      :- humedad(X, Pct), Pct < 50.

ventisca(X)  :- velocidad_viento(X, Velocidad), Velocidad >= 10.
sin_viento(X) :- velocidad_viento(X, Velocidad), Velocidad < 10.

nublado(X)   :- clouds(X, Pct), Pct >= 50.
despejado(X) :- clouds(X, Pct), Pct < 50.

%%%%%%%%%%%%%%%%%%%%
% Climas generales %
%%%%%%%%%%%%%%%%%%%%

clima_calido(X)   :- caliente(X), despejado(X), sin_viento(X).
clima_templado(X) :- templado(X), nublado(X), not(lloviendo(X)).
clima_polar(X)    :- frio(X), nevando(X).

%%%%%%%%%%%%%%%%%%%%%%
% Climas específicos %
%%%%%%%%%%%%%%%%%%%%%%

clima_tropical(X) :- clima_calido(X), humedo(X).
clima_seco(X)     :- despejado(X), soleado(X).
clima_moderado(X) :- templado(X), estable(X), sin_viento(X), soleado(X).


%%%%%%%%%
% Biome %
%%%%%%%%%

% Y is latitude %

tundra(X, Y) :- clima_polar(X) , Y >= 60 , Y <= 75.
bosque(X, Y) :- clima_templado(X), Y >= 35 , Y <= 55.
selva(X, Y)  :- clima_tropical(X), Y >= 0 , Y <= 10.
pradera(X)   :- clima_templado(X) ; clima_tropical(X) , not(bosque).
desierto(X)  :- clima_seco(X), seco(X).
taiga(X)     :- clima_polar(X), gelido(X).
sabana(X)    :- clima_tropical(X), pradera(X).
