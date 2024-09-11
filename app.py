from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)


Pc = 10  # Critical pressure in MPa
vc_liquid = 0.0035  # Critical specific volume of liquid in m^3/kg
vc_vapor = 0.0035  # Critical specific volume of vapor in m^3/kg

# Expanded phase data
phase_data = {
    0.01: {"specific_volume_liquid": 0.001, "specific_volume_vapor": 14.67},
    1: {"specific_volume_liquid": 0.001043, "specific_volume_vapor": 0.1943},
    5: {"specific_volume_liquid": 0.001156, "specific_volume_vapor": 0.03928},
    Pc: {"specific_volume_liquid": vc_liquid, "specific_volume_vapor": vc_vapor},
}

def interpolate(p):
    pressures = np.array(list(phase_data.keys()))
    v_liquids = np.array([data["specific_volume_liquid"] for data in phase_data.values()])
    v_vapors = np.array([data["specific_volume_vapor"] for data in phase_data.values()])
    
    v_liquid = np.interp(p, pressures, v_liquids)
    v_vapor = np.interp(p, pressures, v_vapors)
    
    return v_liquid, v_vapor

@app.route('/phase-change-diagram')
def phase_change_diagram():
    try:
        pressure = float(request.args.get('pressure'))
        if pressure <= 0 or pressure > Pc:
            return jsonify({"error": "Pressure out of range"}), 400
        
        v_liquid, v_vapor = interpolate(pressure)
        
        return jsonify({
            "specific_volume_liquid": round(v_liquid, 7),
            "specific_volume_vapor": round(v_vapor, 5)
        })
    except ValueError:
        return jsonify({"error": "Invalid pressure value"}), 400

if __name__ == '__main__':
    app.run(debug=True)