import numpy as np
from constants import k_e

# distance between two atoms
def distance(atom_i, atom_j):
    r_vec = atom_i.position - atom_j.position
    return np.linalg.norm(r_vec)

# Lennard-Jones 12-6 potential between atoms, menggunakan Lorentz–Berthelot mixing rule
def lj_potential(r, sigma, epsilon):
    sr = sigma / r
    sr6 = sr ** 6
    sr12 = sr6 ** 2
    return 4 * epsilon * (sr12 - sr6)

def lj_lb(r, atom_i, atom_j):
    sigma = (atom_i.sigma + atom_j.sigma) / 2
    epsilon = np.sqrt(atom_i.epsilon * atom_j.epsilon)
    return lj_potential(r, sigma, epsilon)

# coulomb energy
def coulomb_energy(r, q_i, q_j):
    return k_e * (q_i * q_j) / (r + 1e-12)

# total energy
def compute_total_energy(Box):
    E_total = 0.0
    molecules = Box.molecules
    
    # loop molecules
    for i in range(len(molecules)):
        for j in range(i + 1, len(molecules)):

            molc_i = molecules[i]
            molc_j = molecules[j]

            # loop atom antar molecules
            for atom_i in molc_i.atoms:
                for atom_j in molc_j.atoms:

                    r = distance(atom_i, atom_j)

                    if atom_i.charge != 0.0 and atom_j.charge != 0.0:
                        E_total += coulomb_energy(atom_i.charge, atom_j.charge, r)

                    if atom_i.name == "O" and atom_j.name == "O":
                        E_total += lj_lb(r, atom_i, atom_j)
    return E_total