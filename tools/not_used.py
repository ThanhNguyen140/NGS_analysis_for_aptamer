import tools.ngs_tools as ngst
import tools.sql_tools as sqlt
import tools.export_tools as expt


def update_rr_seq_row(conn, table, name_value, update_value):
    """
    SQL query to update rr_seq column in a given table
    :param conn: connection to sql db
    :param table: table name to be updates
    :param name_value: row value with in column "name" to be updated
    :param update_value: New value to replace the original value
    :return: None; updates existing sql table
    """

    update_row = f'UPDATE {table} ' \
                 f'SET rr_seq = "{update_value}"' \
                 f'WHERE ' \
                 f'name = "{name_value}";'
    conn.execute(update_row)
    conn.commit()

def add_rr_seq_column(conn, table):
    """
    Creates a new column named "rr_seq" on a given table
    :param conn: connection to sql db
    :param table: name of table for column to be added upon
    :return: None; new column in existing sql table
    """
    query = f'ALTER TABLE {table} ' \
            f'ADD rr_seq VARCHAR;'
    conn.execute(query)


def reverse_complement_query(conn, round_num):
    """
    SQL query that creates a temporary table (round_#_rev_comp) before combining to the same forward round# table.
    Runs after creating the round_#_rev table for converting the reverse sequences into their complement.
    :param conn: connection to sql db
    :param round_num: table round number that will be converted
    :return: None; creates new sql table
    """


    conn.create_function("strrev", 1, lambda s: s[::-1])
    seq_comp = f"strrev(replace(replace(replace(replace(replace(replace([rr_seq],'A', '?')," \
               f" 'T', 'A'), '?', 'T'), 'G', '!'), 'C', 'G'), '!', 'C'))"
    # cur = conn.cursor()
    # print(len(cur.execute(f'''SELECT strrev({seq_comp}) FROM raw_data ''').fetchall()))

    rev_query = f'CREATE TABLE round_{str(round_num)}_rev_comp AS ' \
                f'SELECT [name], [sequence], [description], {seq_comp} as rr_seq ' \
                f'FROM round_{str(round_num)}_rev '

    conn.execute(rev_query)



def replace_str_index(seq, index=0, replacement='_'):
    return '%s%s%s'%(seq[:index], replacement, seq[index+1:])


def delete_sequence(conn, table, seq, column):
    query = f"DELETE FROM {table} WHERE {column}='{seq}';"
    conn.execute(query)
    conn.commit()


def export_all_sql_tables_to_xls(conn, out_path=r"C:\Users\Bryce\OneDrive\Work\AptaNext-BF\scratch"):
    table_list = sqlt.get_table_names(conn)

    for t in table_list:
        expt.sql_to_xlsx(conn, t, out_path + "\\" + t +".xls")


def remove_unique_seqs(conn,  table, column="rr_seq_count", threshold=10):
    query = f"DELETE FROM {table} WHERE {column} < {threshold};"
    conn.execute(query)
    conn.commit()


def get_total_num_of_seqs(conn, table):
    query = f"SELECT * FROM {table};"

    num_seqs = len([x for x in conn.execute(query)])

    return num_seqs