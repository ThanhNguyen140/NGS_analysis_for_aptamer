# manage_db.py
"""
The "control_panel" folder contains modules that connect the user interface (GUI folder) modules with
the tool modules (tools folder).
-----------------------------------------------------------------------------------------------------
This module is used to manage the connection and the creation of the SQL database
"""
# This module might be not necessary anymore
from constants import MOTIF_SRCH_FOLDER
import sqlite3
import control_panel.manage_params as mp


def create_connection(db_path):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_path: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)

    return conn


#def create_db_ngs(quality=False):
    #"""
    #:param quality: if True; the quality information from the fastq file will be imported to the db
    #:return: None; Creates SQL database from parameters stored in the tmp files
    #"""
    #params = mp.get_parameters_ngs() # get ngs parameters from tmp folder
    #print(params)
    #print(params['files'], params['output'], params['project_name'], quality)
    #fastq_to_sql(params['files'], params['output'], params['project_name'], quality)


#def create_motif_search_db(fastq):
    #fastq_to_sql(fastq, MOTIF_SRCH_FOLDER, 'motif_srch.db')
    


def db_connection():
    """
    Another connection function to current SQL db; w/out arguments
    Used only for "close_connection" function
    :return: con; connection to db to pass to "close_connection"
    """
    db_path = mp.get_current_db_path()
    con = create_connection(db_path)
    return con

def close_connection():
    """
    Closes current connection to SQL database
    :return: None; closes SQL server instance
    """
    con = db_connection()
    con.close()


def delete_tables():
    con = db_connection()
    cursor = con.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "raw_data";')
    #print(cursor.fetchall())
    tables = [x[0] for x in cursor.fetchall()]
    print(tables)

    for table in tables:
        query = f'DROP TABLE {table};'
        print(query)
        con.execute(query)
        con.commit()


