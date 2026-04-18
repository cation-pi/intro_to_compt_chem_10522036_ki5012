import numpy as np
import json
from molecule import Atom, Molecule, Box
from forcefield import compute_total_energy

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def get_xyz(ref, key):
    return np.array([ref[key]["x"],ref[key]["y"],ref[key]["z"]], dtype=float)

def build_water(params, offset_pos): 
    offset = np.array(offset_pos, dtype=float)

    ip = params["interaction_parameters"]
    ref = params["reference_coordinates"]

    O = Atom(
        name="O", 
        position=get_xyz(ref, "O") + offset,
        charge=ip["O"]["charge"],
        sigma=ip["O"]["sigma"],
        epsilon=ip["O"]["epsilon"]
    )

    H1 = Atom(
        name="H1", 
        position=get_xyz(ref, "H1") + offset,
        charge=ip["H"]["charge"],
        sigma=ip["H"]["sigma"],
        epsilon=ip["H"]["epsilon"]
    )

    H2 = Atom(
        name="H2", 
        position=get_xyz(ref, "H2") + offset,
        charge=ip["H"]["charge"],
        sigma=ip["H"]["sigma"],
        epsilon=ip["H"]["epsilon"]
    )


    M = Atom(
        name="M", 
        position=get_xyz(ref, "M") + offset,
        charge=ip["M"]["charge"],
        sigma=ip["M"]["sigma"],
        epsilon=ip["M"]["epsilon"]
    )

    return Molecule([O, H1, H2, M], name="H2O")

if __name__ == "__main__":