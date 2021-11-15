import glob
import os
import pandas as pd

def get_the_newest_file_from_dir(path: str, file_format = None ) -> str:
    if file_format:
        pathforglob = path + '*.' + file_format
    else:
        pathforglob = path + '*'
    list_of_files = glob.iglob(pathforglob)  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

path = 'C:\\Users\\USER\\Documents\\'
file_format = 'csv'

print(get_the_newest_file_from_dir(path,file_format))


df = pd.read_csv(get_the_newest_file_from_dir(path,file_format), sep=";")