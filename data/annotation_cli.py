import pandas as pd
from argparse import ArgumentParser
import sys

DELIM = "------------------------------------------------------------------------------------------------"
LEGEND = "Fantasy - 1 // Horror/Thriller - 2 // Mystery - 3 // Comedy - 4 // Documentary - 5\nAction/Adventure - 6 // Crime - 7 // Romance - 8 // Drama - 9 // Sci-fi - 10 // Western - 11"

def main():
    parser = ArgumentParser()
    parser.add_argument("-s", "--second-annotation", action="store_true", help="File is to be annotated a second time")
    parser.add_argument("--data-path", required=True, type=str, help="Relative path to csv file to annotate")

    args = parser.parse_args()

    movie_data = pd.read_csv(args.data_path, na_filter=False)

    # Based on arg, set the column of the csv to add labels to
    # Also check whether needed column is present.
    write_column = None
    if (args.second_annotation):
        write_column = 'second_label'
    else:
        write_column = 'first_label'
    if (write_column not in movie_data.columns): 
        sys.exit("CSV file does not have needed column (mismatch: check file and input args!)")

    for index, row in movie_data.iterrows():
        if (row[write_column] != 'null'):
            # already been labelled; skip.
            continue

        print(DELIM)
        print(f"Instance #{index}:")
        print(f"\tTitle: {row['title']}")
        print(f"\tPlot:  {row['plot']}\n\n")
        print(LEGEND)

        # Loop until a suitable label is obtained.
        label = None
        while (label == None):
            label_input = input("\nYour label: ").strip()
            if (len(label_input) > 1 or label_input.isdigit() != True): print("Input must be a number from 1-11 (see legend above)!")
            else: 
                match label_input:
                    case "1": label = "Fantasy"
                    case "2": label = "Horror/Thriller"
                    case "3": label = "Mystery"
                    case "4": label = "Comedy"
                    case "5": label = "Documentary"
                    case "6": label = "Action/Adventure"
                    case "7": label = "Crime"
                    case "8": label = "Romance"
                    case "9": label = "Drama"
                    case "10": label = "Sci-fi"
                    case "11": label = "Western"
                    case _: print("Input must be a number from 1-11 (see legend above)!")

        movie_data.at[index, write_column] = label
        movie_data.to_csv(args.data_path, index=False) # Dump/Save all rows as we go.
        print("Saved!")

if __name__ == "__main__":
    main()
