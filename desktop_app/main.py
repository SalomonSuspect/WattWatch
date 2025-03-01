import pathlib

from file_parser import parse_csv
def main():
    path_to_csv = pathlib.Path(input("path to csv file: "))
    for item in parse_csv(path_to_csv):
        print(item)


if __name__ == "__main__":
    main()
