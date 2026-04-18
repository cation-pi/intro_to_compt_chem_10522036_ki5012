import numpy as np

class Atom:
    def __init__(self, name, position, charge=0.0, sigma=0.0, epsilon=0.0):
        self.name = name
        self.position = np.array(position, dtype=float)
        self.charge = charge
        self.sigma = sigma
        self.epsilon = epsilon

    def __repr__(self):
        return (f"Atom({self.name}, pos={self.position}, "
                f"q={self.charge}, sigma={self.sigma}, epsilon={self.epsilon})")

class Molecule:
    def __init__(self, atoms, name=""): 
        self.atoms = atoms
        self.name = name 
    
    def __repr__(self):
        return f"Molecule({self.name}, n_atoms={len(self.atoms)})"

class Box:
    def __init__(self, molecules):
        self.molecules = molecules

    def get_all_atoms(self):
        atoms = []
        for mol in self.molecules:
            atoms.extend(mol.atoms)
        return atoms
    
    def __repr__(self):
        return f"Box(n_molecules={len(self.molecules)})"