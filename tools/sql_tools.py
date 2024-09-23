from sqlalchemy import create_engine
import sqlite3


def create_sql_engine(db_path):
    print('CREATING SQL ENGINE')
    create_engine(f'sqlite:///{db_path}')
    print('ENGINE CREATED')

def text_to_sql(db_path, table_name, columns, txt_file, create_eng=True):
    
    if create_eng:
        create_sql_engine(db_path)

    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute(f'CREATE TABLE {table_name} ({",".join(columns)})')

    with open(txt_file) as f:
        seqs = [cur.execute(f"INSERT INTO {table_name} (name, sequence) VALUES {(x+1, y.strip())}") for x, y in enumerate([v for v in f if v.strip()])]
        #in_query = f"INSERT INTO {table_name} (name, sequence) VALUES (%s, %s)"
        #cur.execute(in_query, seqs)
        conn.commit()

#text_to_sql('test.db', 'raw_data', ['name', 'sequence','description', 'quality_score', 'file_name'], r'/home/ngs_analysis/Desktop/testing/d_round_1.txt')
            

def get_column_names(conn, table):
    """
    SQL query to retrieve all column names from a given table
    :param conn: connection to sql db
    :param table: name of table to retrieve column names
    :return: column names (list)
    """

    query = f'SELECT * FROM {table}'
    cur = conn.execute(query)
    column_names = [description[0] for description in cur.description]
    return column_names


def get_table_names(conn):
    """
    Creates a list of all tables within the sql database
    :param conn: connection to sql database
    :return: list of table names
    """
    query = '''SELECT name FROM sqlite_master WHERE type = 'table';'''
    c = conn.cursor()
    tables = [j[0] for j in c.execute(query)]
    return tables



def check_column_names(conn, table, cols):
    exist_cols = get_column_names(conn, table)
    if (all(x in exist_cols for x in cols)):
        return True
    else:
        return False


def create_sql_table(conn, table, cols, new_table, grp_by=None, ord_by=None):
    cols = ", ".join(cols)
    end = ''

    if grp_by:
        end += f'GROUP by {grp_by} '

    if ord_by:
        end += f'ORDER BY {ord_by} '

    #print(end)
    query = f'CREATE TABLE {new_table} AS ' \
            f'SELECT {cols} FROM {table} ' \
            f'{end}'

    #print(query)

    conn.execute(query)


def get_column_values(conn, table, cols: list, grp_by=None, ord_by=None):

    cols_exist = check_column_names(conn, table, cols)

    if cols_exist:
        cols = ", ".join(cols)
        end = ''

        if grp_by:
            end += f'GROUP by {grp_by} '

        if ord_by:
            end += f'ORDER BY {ord_by} '

        query = f'SELECT {cols} FROM {table} ' \
                f'{end}'

        col_values = [x for x in conn.execute(query)]

        return col_values

def create_select_query(conn, table, cols, where=None, grp_by=None, ord_by=None):

    cols_exist = check_column_names(conn, table, cols)

    if cols_exist:
        cols = ", ".join(cols)
        end = ''

        if where:
            end += f"WHERE {where} "

        if grp_by:
            end += f'GROUP by {grp_by} '

        if ord_by:
            end += f'ORDER BY {ord_by} '


        query = f'SELECT {cols} FROM {table} ' \
                f'{end}'
        #print(query)
        return query

    else:
        print("Cannot find one or more columns")

