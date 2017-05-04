from django.utils import encoding
from pandas import DataFrame
import pandas as pd
import argparse
import os
from pandas import ExcelWriter


parser = argparse.ArgumentParser(description='convert tweets text to excel format')
parser.add_argument('-i', '--infile', type=str,
                    help='input file (csv format).', required=True)
parser.add_argument('-o', '--outfile', type=str,
                    help='output file (excel format).', required=True)
parser.add_argument('-d', '--delimiter', type=str,
                    help='field delimiter.', required=True)
parser.add_argument('-l', '--lines-number', type=int,
                    help='number of lines per excel file', required=True)


# input - df: a Dataframe, chunkSize: the chunk size
# output - a list of DataFrame
# purpose - splits the DataFrame into smaller of max size chunkSize (last is smaller)
def split_dataframe(df, chunk_size=1000):
    list_of_df = list()
    number_chunks = len(df) // chunk_size + 1
    for i in range(number_chunks):
        list_of_df.append(df[i*chunk_size:(i+1)*chunk_size])
    return list_of_df


def export_text2xlsx(infile, outfile, field_delimiter, number):
    df = pd.read_csv(infile, delimiter=field_delimiter, engine='python')
    rows_number = df.shape[0]
    if rows_number > number:
        data_frames = split_dataframe(df, number)
        frame_number = 1
        for frame in data_frames:
            filename, ext = os.path.splitext(outfile)
            excel_file = "{}_{}.xlsx".format(filename, frame_number)
            writer = ExcelWriter(excel_file, engine='xlsxwriter')
            frame.to_excel(writer, 'sheet1')
            writer.save()
            frame_number += 1
    else:
        writer = ExcelWriter(outfile)
        df.to_excel(writer, 'sheet1')
        writer.save()


if __name__ == '__main__':
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    delimiter = args.delimiter
    lines_number = args.lines_number
    export_text2xlsx(infile, outfile, delimiter, lines_number)