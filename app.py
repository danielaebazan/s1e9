from flask import Flask, request, jsonify

app = Flask(__name__)


Pc = 10 # Presión crítica en MPa
vc_liquid = 0.0035 # Volumen específico del líquido en m^3/kg
vc_vapor = 0.0035 # Volumen específico del vapor en m^3/kg

# Diccionario que simula la curva de cambio de fase en función de la presión
phase_data = {
    0.05: {"specific_volume_liquid": 0.00105, "specific_volume_vapor": 0.03},
    10: {"specific_volume_liquid": vc_liquid, "specific_volume_vapor": vc_vapor},
}

# Ruta para obtener el diagrama de cambio de fase
@app.route('/phase-change-diagram')
def phase_change_diagram():
    pressure = float(request.args.get('pressure'))

    # Verifica si la presión está en los datos
    if pressure in phase_data:
        # Devuelve el volumen específico de líquido y vapor
        return jsonify({
            "specific_volume_liquid": phase_data[pressure]["specific_volume_liquid"],
            "specific_volume_vapor": phase_data[pressure]["specific_volume_vapor"]
        })
    else:
        return jsonify({"error": "Pressure data not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
