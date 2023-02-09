import static_objects
import pandas

def main():
    '''
    This functions purpose is to take the user input, like what type of create what thickness etc and send those variables to neccessary
    places to create the proper amount of foils.
    Next we will the necessary functions to create the RIBO input file -- Not quite sure how we format that yet.
    '''
    tar_cont = static_objects.target_container()
    print(tar_cont)
    with open('./test.csv', 'w') as file:
        file.write(str(tar_cont))
        

if __name__ == "__main__":
    main()

