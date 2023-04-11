# TRIUMF

## Team Members
- Benny Cao
- Uday Chhina
- Tyler Grande
- Dennis Phan
- Kevin Xu
- Aaron Zhang
- Brandon Woo

---

## Introduction

This manual serves as a guide to run Python scripts to run simulations for the effusion rate of Be-14 isotope through different geometries of a target container. The simulations are run by the RIBO (Radioactive Ion Beam Optimizer) program which was developed by CERN. While technically the program does not need any python scripts to run the simulations, it does need each of the surfaces to be defined individually through which the effusion rate of the particles is to be determined. 

As the number of surfaces grows in the simulations, so does the input
required. It can get very painstakingly tedious to detail hundreds of surfaces
manually which is why this process has been automated with the help of Python
(to create the input files with the list of all the surfaces and cells). As an
example, the input file for 470 surfaces shaped like a D would look like this:

```txt
Surfaces														
#	rc	T (K)	x2	y2	z2	xy	xz	yz	x	y	z	C		
1	1	2300	1	1.000000000	0	0	0	0	0.000000000	0.000000000	0	0.836127360		
2	1	2300	1	0.000000000	1	0	0	0	-1.906000000	0.000000000	0	-0.863688000		
3	1	2300	1	0.000000000	1	0	0	0	-1.906000000	0.000000000	0	-0.886200000		
4	1	2300	1	-0.361000000	1	0	0	0	-1.906000000	-0.202200000	0	-0.879900000		
5	1	2300	0	0.000000000	0	0	0	0	0.000000000	1.000000000	0	-0.228000000		
6	1	2300	0	0.000000000	0	0	0	0	0.000000000	1.000000000	0	1.040000000		
7	1	2300	0	0.000000000	0	0	0	0	0.000000000	1.000000000	0	5.956000000		
8	1	2300	0	0.000000000	0	0	0	0	1.000000000	0.000000000	0	0.525000000		
9	1	2300	0	0.000000000	0	0	0	0	0.000000000	0.000000000	1	-1.700000000		
10	1	2300	0	0.000000000	0	0	0	0	0.000000000	0.000000000	1	1.700000000		
11	1	2300	0	0.000000000	0	0	0	0	0.000000000	0.000000000	1	-1.695276008		
12	1	2300	0	0.000000000	0	0	0	0	0.000000000	0.000000000	1	-1.692776008		
...
```

```txt
...
949	1	2300	0	0.000000000	0	0	0	0	0.000000000	0.000000000	1	1.692776008		
950	1	2300	0	0.000000000	0	0	0	0	0.000000000	0.000000000	1	1.695276008		
														
Cells														
number	S1	S2	S3	S4	S5									
1	1	-2	-6	-4	5									
2	-3	-7	6	0	0									
3	-1	9	-10	8	0									
4	-1	9	-11	-8	0									
5	-1	12	-13	-8	0									
6	-1	14	-15	-8	0									
7	-1	16	-17	-8	0									
8	-1	18	-19	-8	0									
9	-1	20	-21	-8	0									
10	-1	22	-23	-8	0									
11	-1	24	-25	-8	0									
12	-1	26	-27	-8	0									
...
```

```txt
...
473	-1	948	-949	-8	0									
474	-1	950	-10	-8	0									
														
Source														
type	Mass	T (K)	Alpha	nx	ny	nz	x	y	z	R	L	sigma	theta	phi
T	8	2300	180	0	0	1	0	0	0	0.9144	3.4	0.5	0	90
														
Tally														
S	Nmax	Tmax	Tpmax											
7	1000	1000	10											
```


This goes on for a few hundred lines and is very tedious to write manually. 


---

## Installation and Setup

The current directory with all the files looks like this:

```txt
new files
│   ├── bennygapstuff.py
│   ├── cells
│   │   └── ext-cell.txt
│   ├── foilmath.py
│   ├── inputs.py
│   ├── main.py
│   ├── static
│   │   ├── exterior.txt
│   │   └── foilcut.txt
│   └── static_objects.py
```
[to be changed when finished]

This will be the working directory through which we will be running the python scripts to create the input files for the RIBO program. All files will be provided in a package which can be easily downloaded and placed in the RIBO directory.

Further sections in the manual will explain what each file does and how to
make changes if necessary.

---

## System Documentation

### Files

`main.py`

This is the main python file through which we will be running the script to create the input files for the RIBO program. This file does a few things:

1. `write_csv()`: This function writes the csv for all the components of the
   input file. This funcitons is reused multiple times to write the surfaces,
   cells, tally, and source files. The function takes in the name of the file
   and the number of rows that are being written to the file.

2. `main()`: This is the main function that first sets up all the headers for
   the input file. This includes the surfaces section, the cells sections, the
   source section, and the tally section.The function then calls the
   write_csv() function to write the rows for each of the sections.

`inputs.py`

This file is used to get all the input parameters for running the main file
from the CLI. 

1. `get_foil_options()`: There are multiple parameters like the quantity of
   the foils, the shape (default is D), length of the target container, the
   filename for the input file (target), height of the foils from the origin
   (center of the container), and so on. The full list of the parameters can
   be found in the file itself or by running the command `python inputs.py -h`
   in the CLI.
   
2. `get_anything_else()`: This function reserves the option for users to add
   any other options to the dictionary of parameters. This is useful if the
   simulations require any other parameters that are not included in the
   default values. 

3. `validate()`: This function validates the inputs that are passed
   through the CLI. It checks if the inputs are of the correct type and if
   they are within the correct range. If the inputs are not valid, the
   function will raise an error and exit the program.

An example of the inputs that can be passed through the CLI is shown below:

```bash 
$ python inputs.py --shape D --quantity 470 --height 0.5 --length 1.0 --filename target ... <all other settings>
```

This allows for the test to be run with different parameters without having to
change the python files for each simulation itself.

`static_objects.py`

This file sets up the static parts of the input file. This includes things
like the global temperature, the maximum number of runs for the simulations,
the mass of the foils, and so on. The full list of the parameters can be found
inside the file. 
 The file also sets up a dictionary with all the static headers for the input
 file:

```python
dic = {"Mass":mass,
        "T (K)":temp,
        "Source Headers (T)":["type","Mass","T (K)","Alpha","nx","ny","nz", "x","y","z","R","L","sigma","theta","phi"],
        "Tally Headers":["S","Nmax","Tmax","Tpmax"],
        "Nmax":Nmax
        }
```

This dictionary is used in the main file to write the headers for the input
file.

The file also sets up a dictionary with the names of all the shapes that have
fortran files made and ready to go. The fortran files are needed to generate
the isotope particles in the correct locations for the simulations. Namely,
in the gaps in the foils, or on the foils themselves. This dictionary is also
used to validate the inputs passed through the CLI by checking if it exists in
the dictionary of all the shapes. For example, the names of the d-shaped foils:

```python
shapes = {
        "d_list": ['D','d','D-shaped','d-shaped'],
        # more shapes...
        }
```

Other functions in the file:

1. `format_title()`: This function formats the header titles to have exactly
   15 columns which is required for the RIBO input file to function correctly.

2. `target_container()`: Defines the static surfaces for the
   target container which contains the foils. This funciton reads in the
   information from a txt file called `exterior.txt` which contains the static
   information for the container. 

3. `cells_target_container()`: Defines the static cells for the
   target container which contains the foils. This funciton reads in the
   information from a txt file called `ext-cell.txt` which contains the static
   information for the container.

4. `cell_gaps()`: Calculates the gaps for the foils in terms of the cells for
   the input file.

5. `source()`: Defines the static source for the input file. This funciton
   reads in the information from a txt file called `foilcut.txt` which
   contains the static information for the source.

6. `tally()`: Defines the static tally for the input file. 

---

## Running the Program

To run the program, the user must first have the RIBO program licensed and
installed. The downloaded package must be placed in the RIBO directory. This
way when the program is run, the RIBO program will be able to find the target
input files to run the simulations.

The program can be run by typing the following command in the CLI:


---

## Deployment

---

## Performance Testing







	

