from argparse import ArgumentParser
import os
import pandas as pd

NAMES = ["Lily", "Nour", "Sriya", "Daniel"]
INITIAL_ANNOTATION_SIZE = 250
SECOND_ANNOTATION_SIZE = 38
FULL_DATA_PATH = "output.csv"
DIVISION_PATH = "movie_data_"
ANNOTATED_FOLDER = "to_annotate"

def create_divisions(names: list[str], size: int, data_path: str, new_filename: str, folder: str):
    movie_data = pd.read_csv(data_path)
    movie_data['first_label'] = "null" # add new column to store our new annotations.

    divisions = []
    for i in range(0, len(names)):
        # Create a subset of size passed for each name
        divisions.append(movie_data.loc[size*i : size*(i+1) - 1])

    for div, name in zip(divisions, names):
        # Write each subset to a new file with a name appended in passed folder
        newfile_path = folder + "/" + new_filename + name + ".csv"
        div.to_csv(newfile_path, index=False)

def create_doubled_division(filename: str, size: int, file_suffix: str, folder: str):
    movie_data_annotated = pd.read_csv(folder + "/" + filename + ".csv", na_filter=False)

    newfile_path = folder + "/" + filename + file_suffix + ".csv"
    entries = movie_data_annotated.sample(n=size, random_state=42)    # randomly grab (size) entries
    entries['second_label'] = "null"                                  # add new column for second annotation round
    entries.to_csv(newfile_path, index=False)

def main():
    parser = ArgumentParser()
    opts = parser.add_mutually_exclusive_group(required=True)
    opts.add_argument("--create-initial-divisions", action="store_true", 
                      help="Create the initial set of files for annotation")
    opts.add_argument("--create-second-divisions", action="store_true", 
                      help="Create subfile from each annotated file for second round of annotation")
    
    args = parser.parse_args()
    
    if (args.create_initial_divisions):
        create_divisions(NAMES, INITIAL_ANNOTATION_SIZE, FULL_DATA_PATH, DIVISION_PATH, ANNOTATED_FOLDER)

    elif (args.create_second_divisions):
        for name in NAMES:
            filename = DIVISION_PATH + name
            create_doubled_division(filename, SECOND_ANNOTATION_SIZE, "_twice", ANNOTATED_FOLDER)


if __name__ == "__main__":
    main()
