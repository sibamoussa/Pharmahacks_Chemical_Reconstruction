from multiprocessing import freeze_support
from rdkit import Chem
from mordred import Calculator, descriptors

if __name__ == "__main__":
    freeze_support()

    sdf = Chem.SDMolSupplier("data/compound_set2_3d.sdf")

    mols = []

    for mol in sdf:
        if mol:
            mols.append(mol)

    # Create Calculator
    calc = Calculator(descriptors)

    # map method calculate multiple molecules (return generator)
    print(list(calc.map(mols)))

    # pandas method calculate multiple molecules (return pandas DataFrame)
    #print(calc.pandas(mols))

    # save data frame
    calc.pandas(mols).to_csv("bla.csv")
