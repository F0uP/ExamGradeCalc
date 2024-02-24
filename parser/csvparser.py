import pandas as pd
import csv

def get_delimiter(file_path, bytes = 4096):
    sniffer = csv.Sniffer()
    data = open(file_path, "r").read(bytes)
    delimiter = sniffer.sniff(data).delimiter
    return delimiter

def parse_csv(file_path):
    sep = get_delimiter(file_path)
    return pd.read_csv(file_path, sep=sep, header=0, index_col=0, skipinitialspace=True, skip_blank_lines=True, engine='python')