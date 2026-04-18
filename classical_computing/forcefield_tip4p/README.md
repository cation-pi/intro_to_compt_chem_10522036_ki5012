# implementasi simple force field dari nol untuk TIP4P

## tujuan
1. membangun simple molecular mechanics force field untuk H2O (model TIP4P) dari nol menggunakan python
2. mempelajari molecular simulation engine dan software design secara garis kasar(?)
3. 

## struktur direktori
.  
├── main.py  
├── molecule.py  
├── forcefield.py  
└── tip4p_params.json  

* main.py = main script untuk run programnya.
* molecule.py = mendefinisikan class Atom, class Molecule, dan class System.  
* forcefield.py = berisi fungsi matematika.
* tip4p_params.json = configuration file, berisi parameter TIP4P.

## penjelasan kode
### molecule.py
* class Atom vs class Molecule? atom merupakan unit terkecil, sedangkan molecule adalah satu sistem kecil (kumpulan atom).  
  class Atom seagai data lokal, sedangan Molecule sebagai struktur global. 
* class Box merupakan kumpulan molekul (sistem besar). 
* `class Atom` menyimpan attributes berupa identitas (name), posisi (koordinat), dan physical properties, seperti muatan (q), sigma (collision diameter), dan epsilon (well depth).  
  posisi digunakan untuk menghitung jarak antar atom (r_ij) --> ada di perhitungan energi bond stretching, electrostatics, dan van der Waals.  
  muatan --> dibutuhkan di perhitungan energi elektrostatik.  
  sigma dan epsilon --> dibutuhkan di perhitungan van der Waals.  
* `class Molecule` menyimpan daftar atom (atoms) dan nama molekul (name).
* `position = np.array(position, dtype=float)`. pakai `np.array()` karena akan melakukan operasi vektor pada r_ij. `dtype` artinya data type (tipe data elemen array). harus float karena posisi atom adalah bilangan real.  
  jadi, apapun inputnya (list, tuple), dia mengubah jadi array numerik float.
* `__repr__` adalah dunder method, untuk menentukan bagaimana object ditampilkan saat `print(atom)`. --> mempermudah debugging.


### forcefield.py
constants: 
* `k_e` = coulomb constant (kJ·mol^(-1)·Å·e^(-2)). float. ref: https://wenku.csdn.net/answer/1evu4r5g80 
* `epsilon` = small number untuk menghindari division by zero (r = 0). float
* `r_ij` = jarak euclidean antara dua atom. dalam python, ini merupakan operasi vektor. float. ref: Jensen (2017), eq 2.18


## review materi
* perhitungan force field termasuk ke classical computing karena elektron diabaikan. jadi, bergantung pada fungsi posisi inti (nuclei). --> didasarkan pada Born–Oppenheimer approximation.
* karena termasuk classical, atom dianggap seperti bola, ikatan dianggap seperti pegas --> kontribusinya berupa: bond stretching, angle bending, torsion (rotasi), nonbonded interaction.
* parameter dari small molecule bisa dipakai ke sistem besar (scalable).
* komponen simple force field: `Etotal ​= Ebond ​+ Eangle​ + Etorsion​ + Enonbonded​`
  Ebond = bond stretching --> bisa pakai hooke's law atau morse potential. morse potential bisa untuk bond breaking.  nilainya selalu positif.
  Eangle​ = angle bending --> pakai hooke's law.  nilainya selalu positif.
  Etorsion​ = torsion (dihedral) --> bentuknya cosine periodic. nilainya bisa negatif atau positif. pada beberapa force field, ada yg meniadakan torsion ini karena ga semua sistem punya torsion, jadi digabung ke non-bonded interactions.
  Enonbonded​ = (1) electrostatics (coulomb's law); (2) van der Waals (Lennard-Jones 6-12 potential). 
* parameter-parameter di force field itu harus dari hasil eksperimen atau fitting ke DFT(?)



## references
1. Leach, A. R. (2001) *Molecular Modelling: Principles and Applications* 2nd edn. Harlow: Prentice Hall.
2. Jensen, F. (2017) *Introduction to Computational Chemistry*. John Wiley & Sons.
3. Jorgensen, W.L. et al. (1983) 'Comparison of simple potential functions for simulating liquid water,' *The Journal of Chemical Physics*, 79(2), pp. 926–935. https://doi.org/10.1063/1.445869.
4. Dick, T.J. and Madura, J.D. (2005) 'Chapter 5 A review of the TIP4P, TIP4P-EW, TIP5P, and TIP5P-E water models,' *Annual Reports in Computational Chemistry*, pp. 59–74. https://doi.org/10.1016/s1574-1400(05)01005-4.
5. LAMMPS. *10.4.6. TIP4P and OPC water models*. Tersedia di: https://docs.lammps.org/Howto_tip4p.html.
6. https://pythoninchemistry.org/sim_and_scat/parameterisation/mixing_rules 
7. https://wenku.csdn.net/answer/1evu4r5g80 