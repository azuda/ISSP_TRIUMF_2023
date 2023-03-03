#foil math will prob take the dictionary as a parameter

#just temporary
foil = {
            "foil_quantity": 10, #how many foils will be used in the simulation
            "foil_shape": 'd-shape', #which foil will be created
            "target-file": "path_of_file", 
            "length": 3.4, #main tube length in cm
            "temp": 2300, #temperature
            "foil-height": 0.525, #height of foil from origin
            "thickness": 25, #foil thickness in micron
            "foil-rotation": 0, #rotation of foils
            "ionizer": 5.956, #ionizer length
            "mass": 8, 
            "gradient": None, #temperature gradient used for ionizer
            "NMax": 1000,
            "sep": 0,
            "hsep": 0,
            "squish": 1
            # etc: 'etc'
        }

def foil_math(foil):
    ''''''
    #in microns
    foilThickness = foil['thickness']/10000
    #placeholder this will change accordingly
    foilAmount = foil['foil_quantity'] + 1
    #target chamber itself is 3.4cm 
    containerLength = foil['length']
    foilSpace = foilThickness*foilAmount
    gap = (containerLength - foilSpace)/foilAmount
    return gap, foilAmount
    ### In here we are going to do the foil math, based on thickness relative to the container we will determine the size of the gaps
    #gap equals number of foils times 0.0025, take that subtract from container length
    #divide remaining space by number of foils to get how much the gap needs to be
    #so that the space is even between all foils
    pass

def pizza_foil_gaps(stuff):
    #even number equals foil
    #odd number equals gap
    startingPoint = -1.7
    thickness = 0.0025
    gaps, foilAmount = foil_math(stuff)
    print(foil_math(stuff))
    for i in range(foilAmount):
        if i % 2 == 0: #if number is even 
            #starting from left side, starting with foil 1.7cm away from origin
            #add a foil, so math would be -1.7 + 0.0025
            #goes back to top of loop after
            startingPoint = startingPoint + thickness
            # print(startingPoint)
        else: # if number is odd
            #since foil was added, it should add gap
            #the math would be -1.7 + 0.0025 + however much the gap is
            startingPoint = startingPoint + gaps
            # print(startingPoint)

pizza_foil_gaps(foil)

# if __name__ == "__main__":
#     main()