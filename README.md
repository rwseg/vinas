# vinas - run vina against a directory of ligands with same vina arguments

## Installation

```bash
$ git clone https://github.com/rwseg/vinas.git
$ cd splitdir
$ python setup.py install
```

## NOTE

1. Vinas now support Python 3.x only, if vinas print:

```
AttributeError: 'module' object has no attribute 'run
```

this means your Python version is 2.x, change your Python.

2. Before run vinas, your should has Autodock-Vina installed,
install by Anaconda is recommended:

```bash
$ conda install -c bioconda autodock-vina
```

3. Vinas has 2 kinds of argument, each has its argument prefix

    1. vinas argument: this kind of argument is passed to vinas, argument prefix is +.
    2. vina argument: this kind of argument is passed to vina, argument prefix is -.
    
4. Vina argument is concatenated by =, eg: --receptor=receptor.pdbqt

## Usage

### print help message

```bash
$ vinas ++help
usage: vinas [+h] +l LIGAND +o OUT [+d] +v VINA

run vina against a directory of ligands with same arguments

optional arguments:
  +h, ++help            show this help message and exit
  +l LIGAND, ++ligand LIGAND
                        ligand directory
  +o OUT, ++out OUT     output directory
  +d, ++debug           enable debug mode
  +v VINA, ++vina VINA  vina argument
```

### example

```bash
$ vinas ++l ./zinc-1 +o ./temp +v --receptor=new.pdbqt +v --center_x=20.568 +v --center_y=35.285 +v --center_z=13.029 +v --size_x=28 +v --size_y=28 +v --size_z=40 +v --num_modes=9 +v --energy_range=1
```

### enable debug mode

```bash
$ vinas +d ++l ./zinc-1 +o ./temp +v --receptor=new.pdbqt +v --center_x=20.568 +v --center_y=35.285 +v --center_z=13.029 +v --size_x=28 +v --size_y=28 +v --size_z=40 +v --num_modes=9 +v --energy_range=1
```

