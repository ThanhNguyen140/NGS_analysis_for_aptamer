from tools.not_used import get_total_num_of_seqs
import tools.export_tools as expt
import tools.ngs_tools as ngst
import control_panel.manage_params as mp
import control_panel.manage_db as mdb
import control_panel.manage_ngs as mngs
import matplotlib.pyplot as plt
import numpy as np
import os

# This might be not needed
def export_round_all_seqs_txt():
    db_path = mp.get_current_db_path()
    rounds = mp.get_current_rounds()
    outpath = mp.get_last_output_path()
    con = mdb.create_connection(db_path)
    proj_name = mp.get_current_project_name()
    for rnd in rounds:
        expt.round_all_seqs_to_txt(con, rnd, outpath, proj_name)

# This might be not needed
def export_round_nr_seqs_txt():
    db_path = mp.get_current_db_path()
    rounds = mp.get_current_rounds()
    outpath = mp.get_last_output_path()
    con = mdb.create_connection(db_path)
    proj_name = mp.get_current_project_name()

    for rnd in rounds:
        expt.round_nr_seqs_to_txt(con, rnd, outpath, proj_name)

# This might be not needed
def export_round_seqs_counts_txt():
    rounds = mp.get_current_rounds()
    conn = mdb.db_connection()
    outpath = mp.get_current_output_path()
    proj_name = mp.get_current_project_name()

    for r in rounds:
        expt.round_seqs_counts_txt(conn, r, outpath, proj_name)

# This might be not needed
def export_all_rounds_nr_seqs_txt():
    conn = mdb.db_connection()
    outpath = mp.get_current_output_path()
    proj_name = mp.get_current_project_name()

    expt.all_rounds_nr_seqs_txt(conn, outpath, proj_name)


def export_unique_seqs_all_rounds(df):
    rnds = mp.get_current_rounds()
    rounds = [int(r) for r in rnds]
    outpath = mp.get_last_output_path()
    proj_name = mp.get_current_project_name()
    ngst.plot_unique(df,rounds)
    plt.savefig(os.path.join(outpath,f'{proj_name}_unique_plot.png'))
    plt.close()
        
# This might be not needed
def export_round_tables_to_txt():
    rounds = mp.get_current_rounds()
    conn = mdb.db_connection()
    outpath = mp.get_current_output_path()
    proj_name = mp.get_current_project_name()
    for r in rounds:
        expt.round_all_seqs_to_txt(conn, r, outpath, proj_name)

# This might be not needed
def export_round_counts_to_txt():
    rounds = mp.get_current_rounds()
    db_path = mp.get_current_db_path()
    outpath = mp.get_last_output_path()
    proj_name = mp.get_current_project_name()
    con = mdb.create_connection(db_path)


    with open(os.path.join(outpath, f'{proj_name}_seq_counts_per_round.txt'), 'w') as file:
        file.write('Sequence Counts per Round\n\n\n')
    
    with open(os.path.join(outpath, f'{proj_name}_seq_counts_per_round.txt'), 'a') as file:

        for rnd in rounds:
            tot_num = get_total_num_of_seqs(con, f'round_{rnd}')
            file.write(f'round {rnd}:\n{tot_num}\n\n\n')

