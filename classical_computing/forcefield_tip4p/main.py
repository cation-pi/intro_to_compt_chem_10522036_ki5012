import numpy as np
import json
from molecule import Atom, Molecule, Box
from forcefield import compute_total_energy

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def validate_tip4p_params(params):
    required_keys = ["metadata","interaction_parameters","geometry_parameters","reference_coordinates"]

    for key in required_keys:
        if key not in params:
            raise ValueError(f"missing key in parameter file: {key}")

    units = params["metadata"]["units"]

    if units["distance"] != "Angstrom":
        raise ValueError("distance unit must be Angstrom")

    if units["charge"] != "e":
        raise ValueError("charge unit must be e")


def get_xyz(ref, atom_key):
    return np.array([ref[atom_key]["x"],ref[atom_key]["y"],ref[atom_key]["z"]], dtype=float)

# one molecule builder
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
        name="H",
        position=get_xyz(ref, "H1") + offset,
        charge=ip["H"]["charge"],
        sigma=ip["H"]["sigma"],
        epsilon=ip["H"]["epsilon"]
    )

    H2 = Atom(
        name="H",
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

# placement functions: posisi grid
def generate_grid_positions(nx, ny, nz, spacing):
    positions = []

    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                pos = np.array([i * spacing,j * spacing,k * spacing], dtype=float)

                positions.append(pos)
    
    return positions

# system builder
def build_system(sim_config):
    molecules = []

    ff_map = sim_config["forcefield"]

    for component in sim_config["components"]:

        mol_name = component["molecule"]
        count = component["count"]

        if mol_name not in ff_map:
            raise ValueError(f"no forcefield assigned for molecule: {mol_name}")

        ff_file = ff_map[mol_name]
        params = load_json(ff_file)

        if mol_name == "water":
            validate_tip4p_params(params)

        placement = component["placement"]

        # grid placement
        if placement["method"] == "grid":
            positions = generate_grid_positions(placement["nx"],placement["ny"],placement["nz"],placement["spacing"])

            if count > len(positions):
                raise ValueError("grid slots less than molecule count")

            for i in range(count):

                offset = positions[i]

                if mol_name == "water":
                    mol = build_water(params, offset)
                    molecules.append(mol)

                else:
                    raise ValueError(f"unknown molecule type: {mol_name}")

        else:
            raise ValueError(
                f"unknown placement method: {placement['method']}"
            )

    return Box(molecules)


# main
if __name__ == "__main__":

    sim_config = load_json("simulation.json")

    print("=" * 50)
    print("system name :", sim_config["system_name"])
    print("building system...")
    print("=" * 50)

    box = build_system(sim_config)

    print(f"total molecules : {len(box.molecules)}")

    total_energy = compute_total_energy(box)

    print("-" * 50)
    print(f"total energy = {total_energy}")
    print("-" * 50)