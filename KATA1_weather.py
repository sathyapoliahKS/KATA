from typing import List

import pandas as pd


def compute(name: str, computation: List[str], program: str):
    df = pd.read_fwf(name, line_terminator='\n')
    df[computation] = df[computation].apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True)
    df['temp_spread'] = df[computation.__getitem__(0)].astype(int) - df[computation.__getitem__(1)].astype(int)
    df = df[df.temp_spread > 0]
    print(program, df[df.temp_spread == df.temp_spread.min()]['Dy'].item())


if __name__ == "__main__":
    source_file_name = 'weather.dat'
    cols_for_spread_computation = ['MxT', 'MnT']
    program_intent = 'The day number with the smallest temperature spread is'
    compute(source_file_name, cols_for_spread_computation, program_intent)
