from typing import List

import pandas as pd
import re


def sanitize_data(file_name: str):
    dest_file_name = 'temp_file.dat'
    reading_file = open(file_name, "r")
    new_file_content = ""
    regex = re.compile(r"^\d+\.*")
    for line in reading_file:
        new_line = line.strip().replace("-", "")
        new_line = re.sub(regex, "", new_line)
        new_file_content += new_line + "\n"
    reading_file.close()

    writing_file = open(dest_file_name, "w")
    writing_file.write(new_file_content)
    writing_file.close()
    return dest_file_name


def read_file_into_dataframe(file_name: str):
    return pd.read_fwf(file_name)


def sanitize_dataframe(df):
    df.fillna(0, inplace=True)
    df = df.rename(columns={'A': 'Unknown'})
    df = df.rename(columns={'Unnamed: 7': 'A'})
    return df


def compute(df, computation: List[str]):
    df[computation] = df[computation].apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True)
    df['point_spread'] = df[computation.__getitem__(0)].astype(int) - df[computation.__getitem__(1)].astype(int)
    return df[df.point_spread > 0]


def print_output(program: str, df, required_col_name: str):
    print(program, df[df.point_spread == df.point_spread.min()][required_col_name].item())


if __name__ == "__main__":
    dataframe = read_file_into_dataframe('weather.dat')
    dataframe = sanitize_dataframe(dataframe)
    dataframe = compute(dataframe, ['MxT', 'MnT'])
    print_output('The day number with the smallest temperature spread is', dataframe, 'Dy')
    final_destination_file = sanitize_data('football.dat')
    dataframe = read_file_into_dataframe(final_destination_file)
    dataframe = sanitize_dataframe(dataframe)
    dataframe = compute(dataframe, ['F', 'A'])
    print_output('The name of the team with the smallest difference in ‘for’ and ‘against’', dataframe, 'Team')
