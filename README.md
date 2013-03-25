kvvliveapi
==========

Python Bindings für die API, die von der KVV Live Webapp benutzt wird.

Wenn jemand bindings für andere Sprachen schreiben will: hier die Dokumentation der API. Andere bindings würde ich auch gerne hier verlinken :)

API Dokumentation
=================

Für jeden Request muss der API-Key als GET-Parameter *key* mit übergeben werden. Der Schüssel ist 377d840e54b59adbe53608ba1aad70e8

Die url setzt sich zusammen aus *http://live.kvv.de/webapp/*, dann der Teil für die Anfrage, wie unten erklärt, dann noch ein *?key=API_KEY* (key s.o.)

##Suche

Die Suche liefert ein JSON-Objekt zurück, dass auf oberster Ebene nur das Attribut *stops* hat. Es enthält eine Liste von Haltestellen mit je den Attributen *id*, *name*, *lat* und *lon*)

###Suche nach Lat/Lon

Die Anfrage ist *API_BASE/stops/bylatlon/LAT/LON?key=API_KEY* (ersetze LAT und LON durch die gewünschten Werte)

###Suche nach Name

Die Anfrage ist *API_BASE/stops/byname/NAME?key=API_KEY* (ersetze NAME durch die gesuchten Haltestellennamen (url-Encoding nicht vergessen))

###Suche nach Haltestellen-ID

Die Anfrage ist *API_BASE/stops/bystop/HALTESTELLEN_ID?key=API_KEY* (ersetze HALTESTELLEN_ID durch die ID der gewünschten Haltestelle)


##Abfahrtszeiten

Das JSON hat auf der obersten Ebene die Attribute *timestamp*, *stopName* und *departures*. Letzeres enthält eine Liste von Abfahrten mit den Attributen *route* (Linie), *destination*, *direction* (1 oder 2), *time*, *vehicleType* (immer null???), *lowfloor* (true oder false), *realtime* (ob Echtzeitwerte vorhanden sind), *traction* (Fahrzeugnummer) und *stopPosition* (Gleis?).

###Abfahrt nach Haltestelle

Die Anfrage ist *API_BASE/departures/bystop/HALTESTELLEN_ID?maxInfos=10&key=API_KEY* (ersetze HALTESTELLEN_ID durch die ID der gewünschten Haltestelle, *maxInfos* kann ebenfalls angepasst werden)

###Abfahrt nach Haltestelle und Linie

Die Anfrage ist *API_BASE/departures/byroute/LINIE/HALTESTELLEN_ID?maxInfos=10&key=API_KEY* (LINIE ist z.B. *S2*, Haltestelle wie oben)

