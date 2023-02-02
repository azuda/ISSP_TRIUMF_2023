**K. Watts, Dec 2022**

# The Gist
There are several documents in this directory. The most important are the four
Jupyter notebooks listed and explained in the next section. 

The .txt files are dependencies that hold the geometries of the target chamber 
and ionizer without the foils, since they don't change as the foil shapes change. 
Please leave them where they are so they can be properly called. 

The `Sketches/` directory holds sketches of some of the shapes. They're
referenced in comments in `Inputs.ipynb` and `Inputs.py` where I felt a drawing
would better explain the choices I made. 

The `Plots/` directory holds the generated plots from `Outputs.ipynb`. They're
organized by subdirectories describing the simulation (e.g., `10-Foils/`,
`Arc/`, etc.)

# 4 Jupyter Notebooks 

1. `Geometry.ipynb`
2. `Generating-Inputs.ipynb`
3. `Outputs.ipynb`
4. `Outputs-Archive.ipynb`

## Geometry.ipynb
Use for finding specific parameters for variations on the existing shapes. 
Contains one function: `area`, which takes many parameters. Does not require all
parameters to be called. 

For example, calling the function and passing a mass, shape, and thickness,
will give you the surface area per foil side, total surface area, number of
foils, gap width, and several other parameters.

Full list of parameters and explanations can be found in the file. 

## Generating-Inputs.ipynb
Use to call `Inputs.py`'s main function, which generates input ('target') files
for RIBO.  
Contains template for use and examples of past use. Loops may be implemented to
generate many input files at once.

The `Inputs.ipynb` and `Inputs.py` files contain the same code. The notebook is
provided for a more readable reference within Jupyter. 

If you'd like to add to the `Inputs.py` file, be sure to restart the
`Generating-Inputs.ipynb` function, or else your changes won't be read into the
notebook until the next time it's restarted or reopened.

The `Inputs.py` and `Inputs.ipynb` files refer to sketches to explain certain
choices. These can be found in `Python/Sketches`.

Full list of parameters (including the shape options) and explanations can be 
found in the file.

## Outputs.ipynb
This is the clean post-processing file. Use for creating plots for analysis. 

Contains:
- RIBO's fitting function
- Kurtis' functions 
- Katelyn's functions
- Working example/template for organizing data
- Working example/template for calling some of the plotting functions

All functions are heavily commented, especially their arguments. 

The templates are also heavily commented.

## Outputs-Archive.ipynb
This is the original post-processing file. It has the same functions and
corresponding comments, but rather than a commented template, it has past
usages of the functions and can regenerate existing plots in `Python/Plots/`.  
















 
