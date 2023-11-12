from functools import reduce
from flask import Flask, request, jsonify

app = Flask(__name__)

# Erweiterte Datenstruktur für Autos
autos = {
    '1': {'Marke': 'Toyota', 'Modell': 'Corolla', 'Jahr': 2020, 'Preis': 20000},
    '2': {'Marke': 'Honda', 'Modell': 'Civic', 'Jahr': 2019, 'Preis': 18000}
}

# Basisroute
@app.route('/')
def get_All():
    return jsonify(autos)

# Routen für Autoverwaltung
@app.route('/auto/<string:auto_id>')
def zeige_auto(auto_id):
    return jsonify(autos.get(auto_id, 'Auto nicht gefunden'))

def generate_new_auto_id():
    return str(max([int(k) for k in autos.keys()]) + 1)

@app.route('/add_auto', methods=['POST'])
def add_auto():
    data = request.json
    new_id = generate_new_auto_id()
    autos[new_id] = data
    return jsonify({"status": "Auto hinzugefügt", "id": new_id})

@app.route('/update_auto/<string:auto_id>', methods=['PUT'])
def update_auto(auto_id):
    if auto_id in autos:
        data = request.json
        autos[auto_id].update(data)
        return jsonify({"status": "Auto aktualisiert", "id": auto_id})
    else:
        return jsonify({"status": "Auto nicht gefunden"}), 404

# Hilfsfunktionen
def erhoehe_preise(preis):
    return preis * 1.1

# Route für die Preisberechnung
@app.route('/autos/erhoehte_preise')
def zeige_erhoehte_preise():
    erhoehte_preise = {id: erhoehe_preise(auto['Preis']) for id, auto in autos.items()}
    return jsonify(erhoehte_preise)

# Funktion zur Ausführung einer Aktion
def ausfuehren_aktion(aktion, daten):
    return aktion(daten)

# Speichern von Funktionen in Variablen
aktion_add = add_auto
aktion_update = update_auto

# Verwendung der gespeicherten Funktionen
@app.route('/aktion/add', methods=['POST'])
def route_add_auto():
    return ausfuehren_aktion(aktion_add, request.json)


@app.route('/aktion/update', methods=['POST'])
def route_update_auto():
    return ausfuehren_aktion(aktion_update, request.json)


def manage_auto(action):
    def add_auto(daten):
        # Fügt ein Auto hinzu
        pass

    def update_auto(daten):
        # Aktualisiert ein Auto
        pass

    # Closure, die je nach Aktion eine spezifische Funktion zurückgibt
    if action == 'add':
        return add_auto
    elif action == 'update':
        return update_auto

# Höherwertige Funktion mit Closure
@app.route('/aktion/<string:action>', methods=['POST'])
def route_manage_auto(action):
    action_function = manage_auto(action)
    return action_function(request.json) if action_function else 'Aktion nicht gefunden', 404

modell_gross = lambda id: autos[id]['Modell'].upper() if id in autos else 'Nicht gefunden'

@app.route('/auto_modell_gross/<string:auto_id>')
def zeige_modell_gross(auto_id):
    return jsonify({"Modell": modell_gross(auto_id)})



vergleiche_modelle = lambda id1, id2: autos[id1]['Modell'] == autos[id2]['Modell'] if id1 in autos and id2 in autos else False

@app.route('/vergleiche_modelle/<string:auto_id1>/<string:auto_id2>')
def vergleiche_auto_modelle(auto_id1, auto_id2):
    return jsonify({"Gleiche Modelle": vergleiche_modelle(auto_id1, auto_id2)})



sortiere_nach_jahr = lambda auto_ids: sorted(auto_ids, key=lambda id: autos[id]['Jahr'])

@app.route('/autos/sortiert')
def zeige_sortierte_autos():
    sortierte_auto_ids = sortiere_nach_jahr(autos.keys())
    sortierte_autos = {id: autos[id] for id in sortierte_auto_ids}
    return jsonify(sortierte_autos)

erhoehe_preise = lambda preis: preis * 1.1
erhoehte_preise = map(lambda id: (id, erhoehe_preise(autos[id]['Preis'])), autos.keys())

# Filter: Findet alle Autos über 18000
autos_ueber_18000 = filter(lambda id: autos[id]['Preis'] > 18000, autos.keys())

# Reduce: Berechnet die Gesamtsumme aller Preise
gesamtsumme = reduce(lambda summe, id: summe + autos[id]['Preis'], autos.keys(), 0)

# Flask-Endpunkte, die Map, Filter und Reduce verwenden
@app.route('/autos/erhoehte_preise')
def zeige_erhoehte_preisee():
    return jsonify(dict(erhoehte_preise))

@app.route('/autos/ueber_18000')
def zeige_autos_ueber_18000():
    return jsonify(list(autos_ueber_18000))

@app.route('/autos/gesamtsumme')
def zeige_gesamtsumme():
    return jsonify({"Gesamtsumme": gesamtsumme})


gesamtsumme_erhoehter_preise = reduce(
    lambda summe, preis: summe + preis,
    map(
        lambda preis: preis * 1.1,
        filter(
            lambda preis: preis > 18000,
            [autos[id]['Preis'] for id in autos]
        )
    ),
    0
)

# Flask-Endpunkt
@app.route('/autos/gesamtsumme_erhoeht')
def zeige_gesamtsumme_erhoeht():
    return jsonify({"Gesamtsumme Erhöhter Preise": gesamtsumme_erhoehter_preise})

# Flask-Endpunkt

# Start der Anwendung
if __name__ == '__main__':
    app.run(debug=True)