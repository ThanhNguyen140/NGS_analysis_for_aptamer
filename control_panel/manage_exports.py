import control_panel.manage_params as mp
import control_panel.manage_db as mdb
import tools.export_tools as et

# Needs modification

def export_round_tables_to_txt():
    rounds = mp.get_current_rounds()
    conn = mdb.db_connection()
    outpath = mp.get_current_output_path()
    proj_name = mp.get_current_project_name()
    for r in rounds:
        et.round_all_seqs_to_txt(conn, r, outpath, proj_name)


def export_nr_seqs_to_txt():
    rounds = mp.get_current_rounds()
    conn = mdb.db_connection()
    outpath = mp.get_current_output_path()
    proj_name = mp.get_current_project_name()

    for r in rounds:
        et.round_nr_seqs_to_txt(conn, r, outpath, proj_name)


def export_round_seqs_counts_to_txt():
    rounds = mp.get_current_rounds()
    conn = mdb.db_connection()
    outpath = mp.get_current_output_path()
    proj_name = mp.get_current_project_name()

    for r in rounds:
        et.round_seqs_counts_txt(conn, r, outpath, proj_name)

def export_all_rounds_nr_seqs_txt():
    conn = mdb.db_connection()
    outpath = mp.get_current_output_path()
    proj_name = mp.get_current_project_name()

    et.all_rounds_nr_seqs_txt(conn, outpath, proj_name)


