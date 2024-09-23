import pandas as pd
from xlsxwriter.workbook import Workbook

def read_file(xlsx_file, sheet_name):
    file = pd.ExcelFile(xlsx_file)
    sheet = file.parse(sheet_name)

    print(sheet["NGS"][1])


def export_table_color(out_path, sheet_name, data, col_num=0, headers=None):
    workbook = Workbook(out_path)
    worksheet = workbook.add_worksheet(sheet_name)

    red = workbook.add_format({"color": "#DC0416"})
    orange = workbook.add_format({"color": "#FFA600"})
    blue = workbook.add_format({"color": "blue"})
    green = workbook.add_format({"color": "green"})

    worksheet.set_column('A:AA', 30)
    print('WRITING DATA TO .xlsx FILE')
    for cols in data:
        #if col_num != 0:
            #col_num += 1
        #print('cols', cols)
        for col in cols:
            #print('col', col)
            row_num = 0

            if headers:
                #print(headers)
                for i, v in enumerate(headers):
                    worksheet.write(row_num, i, v)
                row_num +=1

            for sequence in col:
                # Get each DNA base character from the sequence.
                #print('sequence', sequence)
                format_pairs = []

                

                if type(sequence) is int or type(sequence) is float:
                    worksheet.write(row_num, col_num, sequence)
                    row_num += 1

                else:
                    for base in str(sequence):

                        # Prefix each base with a format.
                        if base == 'A':
                            format_pairs.extend((red, base))

                        elif base == "T":
                            format_pairs.extend((green, base))

                        elif base == 'C':
                            format_pairs.extend((blue, base))

                        elif base == 'G':
                            format_pairs.extend((orange, base))

                        else:
                            # Non base characters are unformatted.
                            if len(str(sequence)) == 1:
                                format_pairs.append('_'+str(base))
                            else:
                                format_pairs.append(base)


                    #print(row_num,col_num)
                    worksheet.write_rich_string(row_num, col_num, *format_pairs)
                    row_num += 1

            col_num += 1
    workbook.close()
