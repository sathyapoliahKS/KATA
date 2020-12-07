from typing import List

import pandas as pd
import re


def compute(name: str, computation: List[str], program: str):
    dest_file_name = 'football_edited.dat'
    reading_file = open(name, "r")
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
    df = pd.read_fwf(dest_file_name)

    df.fillna(0, inplace=True)
    df = df.rename(columns={'A': 'Unknown'})
    df = df.rename(columns={'Unnamed: 7': 'A'})

    df[computation] = df[computation].apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True)
    df['point_spread'] = df[computation.__getitem__(0)].astype(int) - df[computation.__getitem__(1)].astype(int)
    df = df[df.point_spread > 0]

    print(program, df[df.point_spread == df.point_spread.min()]['Team'].item())


if __name__ == "__main__":
    source_file_name = 'football.dat'
    cols_for_spread_computation = ['F', 'A']
    program_intent = 'The name of the team with the smallest difference in ‘for’ and ‘against’ goals is'
    compute(source_file_name, cols_for_spread_computation, program_intent)
