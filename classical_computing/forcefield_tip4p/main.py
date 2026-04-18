import numpy as np
import json
from molecule import Atom, Molecule, Box
from forcefield import compute_total_energy

with open("tip4p_params.json", "r") as f: 
    params = json.load(f)
print(params)

def build_water(params, offset_pos): 
    offset = np.array(offset_pos, dtype=float)

    ip = params["interaction_parameters"]
    ref = params["reference_coordinates"]

    O = Atom(
        "O", np.array([ref["O"]["x"],ref["O"]["y"],ref["O"]["z"]]) + offset
        ip["O"]["charge"],
        ip["O"]["sigma"],
        ip["O"]["epsilon"]
    )

    H1 = Atom(
        "H1", np.array([ref["H1"]["x"],ref["H1"]["y"],ref["H1"]["z"]]) + offset
        ip["H"]["charge"],
        ip["H"]["sigma"],
        ip["H"]["epsilon"]
    )

    H2 = Atom(
        "H2", np.array([ref["H2"]["x"],ref["H2"]["y"],ref["H2"]["z"]]) + offset
        ip["H"]["charge"],
        ip["H"]["sigma"],
        ip["H"]["epsilon"]
    )

    M = Atom(
        "M", np.array([ref["M"]["x"],ref["M"]["y"],ref["M"]["z"]]) + offset
        ip["M"]["charge"],
        ip["M"]["sigma"],
        ip["M"]["epsilon"]
    )

    return Molecule([O, H1, H2, M], name="H2O")

