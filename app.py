from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Parámetros de la curva de saturación
Pc = 10 # Presión crítica en MPa
Tc = 500 # Temperatura crítica en °C
vc = 0.0035 # Volumen específico crítico en m^3/kg

# Función para calcular el volumen específico 
def specific_volume(pressure, temperature):
    # Calcula el volumen específico del líquido
    if temperature < Tc:
        v_liquid = vc * (1 - (pressure/Pc)**(1/3))
        return v_liquid

    # Calcula el volumen específico del vapor
    if temperature >= Tc:
        v_vapor = vc * (1 + (pressure/Pc)**(1/3))
        return v_vapor

    return None

# Ruta para obtener el diagrama de cambio de fase
@app.route('/phase-change-diagram')
def phase_change_diagram():
    pressure = float(request.args.get('pressure'))
    temperature = float(request.args.get('temperature'))
    if pressure < 0 or temperature < 0:
        return jsonify({"error": "Presión y temperatura deben ser positivas."})

    # Obtener volúmenes específicos para la presión y temperatura dadas
    v_liquid = specific_volume(pressure, temperature)
    v_vapor = specific_volume(pressure, temperature)

    # Devolver la información en formato JSON
    return jsonify({"specific_volume_liquid": v_liquid, "specific_volume_vapor": v_vapor})

if __name__ == '__main__':
    app.run(debug=True)