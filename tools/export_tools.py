import os
import pandas as pd
import tools.ngs_tools as ngst
import tools.xls_tools as xlt
from Bio import SeqIO
import csv



def df_to_xlsx(df, xl):
    writer = pd.ExcelWriter(xl)
    df.to_excel(writer)
    writer.save()

def df_to_color_xlsx(df, xl):
    headers = df.columns.values.tolist()
    columns = []
    #print(headers)
    for h in headers:
        column = []
        column.append(df[h].tolist())
        columns.append(column)
    #print(columns)
    #print(headers)
    #print(df)
    xlt.export_table_color(xl, 'Summary', columns, headers=headers)

def list_to_xlsx(l, xlsx, sht_name="Sheet1"):
    df = pd.DataFrame(l)
    writer = pd.ExcelWriter(xlsx, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sht_name, index=False, header=False)
    writer.save()




def add_to_freq_table(df, rounds):

    cols = list(df.columns)

    #print(cols)
    df[f"R{rounds[0]}"] = 0
    for i in range(len(cols)-2):
        r = rounds[i+1]
        first = cols[i+1]
        second = cols[i+2]
        df[f"R{r}"] = df[second] / df[first]

    #print(df)


def print_list_to_txt(outfile, itemlist):
    with open(outfile, "w") as outfile:
        outfile.write("\n".join(itemlist))


def round_all_seqs_to_txt(conn, rnd, out_path, proj_name):
    query = f"SELECT rr_seq FROM round_{str(rnd)}"
    seq_list = [i[0] for i in conn.execute(query)]
    #print(seq_list)
    outfile = os.path.join(out_path, f"{proj_name}_round_{str(rnd)}.txt")
    print_list_to_txt(outfile, seq_list)


def round_nr_seqs_to_txt(conn, rnd, out_path, proj_name):
    query = f"SELECT rr_seq FROM round_{str(rnd)}_count"
    seq_list = [i[0] for i in conn.execute(query)]
    #print(seq_list)
    outfile = os.path.join(out_path, f"{proj_name}_round_{str(rnd)}_nr_seqs.txt")
    print_list_to_txt(outfile, seq_list)


def round_seqs_counts_txt(conn, rnd, out_path, proj_name):
    query = f"SELECT * FROM round_{str(rnd)}_count"
    seq_list = [f"{i[0]} {i[1]}" for i in conn.execute(query)]
    #print(seq_list)
    outfile = os.path.join(out_path, f"{proj_name}_round_{str(rnd)}_seqs_counts.txt")
    print_list_to_txt(outfile, seq_list)


def all_rounds_nr_seqs_txt(conn, out_path, proj_name):
    query = f"SELECT * FROM unique_seqs"
    seq_list = [i[0] for i in conn.execute(query)]
    #print(seq_list)
    outfile = os.path.join(out_path, f"{proj_name}_all_nr_seqs.txt")
    print_list_to_txt(outfile, seq_list)



def merge_files(file_list, new_file, file_type):
    with open(new_file, 'w') as w_file:
        for file in file_list:
            with open(file, 'rU') as f:
                seq_records = SeqIO.parse(f, file_type)
                SeqIO.write(seq_records, w_file, file_type)





# if __name__ == '__main__':
#     con = ngst.create_connection(r"C:\Users\Bryce\Desktop\test.db")
#     export_round_counts(con, [1,2,3], r"C:\Users\Bryce\Desktop")
