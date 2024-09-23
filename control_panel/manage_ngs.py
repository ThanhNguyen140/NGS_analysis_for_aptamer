import sys
sys.path.append('..')
import os
from constants import *
import control_panel.manage_params as mp
import control_panel.manage_db as mdb
import tools.misc_tools as mt
import tools.ngs_tools as ngst
import tools.export_tools as expt
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import QThread, pyqtSignal


#def create_db_ngs(quality=False):
    #params = mp.get_parameters_ngs()
    #print(params)
    #print(params['files'], params['output'], params['project_name'], quality)
    #ngst.fastq_to_sql(params['files'], params['output'], params['project_name'], quality)

def no_split_into_rounds():
    db_path = mp.get_current_db_path()
    #print(db_path)
    con = mdb.create_connection(db_path)

    ngst.create_no_split_round_table(con, 'x')

def export_unique_seqs_all_rounds(df):
    rnds = mp.get_current_rounds()
    rounds = [int(r) for r in rnds]
    outpath = mp.get_last_output_path()
    proj_name = mp.get_current_project_name()
    ngst.plot_unique(df,rounds)
    plt.savefig(os.path.join(outpath,f'{proj_name}_unique_plot.png'))



def create_count_tables_rounds_all(df):
    
    params = mp.get_parameters_ngs()
    rounds =  [int(r) for r in params['rounds']]
    outpath = mp.get_last_output_path()
    proj_name = mp.get_project_name_tmp()

    #if os.path.exists(os.path.join(NGS_TEMP_FOLDER, r'count_threshold.ngs')):
        #thresh = int(mp.get_seq_count_threshold())

    #else:
        #thresh = 0
    print('CREATING ROUND COUNT TABLES')
    count_all_rounds = ngst.create_count_seq_all_rounds(df,rounds)
    count_all_rounds.to_csv(os.path.join(outpath,'%s_count_all_rounds.csv'%proj_name), index = False)
    return count_all_rounds


def create_nucleotide_graphs(df):
    rnds = mp.get_current_rounds()
    rounds = [int(r)for r in rnds]
    proj_name = mp.get_current_project_name()
    out_path = mp.get_current_output_path()
    #print(con, rounds, proj_name, out_path)
    per_A = []
    per_C = []
    per_G = []
    per_T = []
    round_col = []
    position = []
    
    for i in rounds:
        df_r = df[['sequence','count_%d'%i]]
        fig = plt.figure(figsize=(10,5))
        A,C,T,G = ngst.graph_nucleotides(df_r,i)
        plt.title('Round %d_%s'%(i,proj_name),size = 14, font = 'arial',fontweight = 'bold')
        plt.savefig(os.path.join(out_path,'%s_nucleotide_plot_R%d.png'%(proj_name,i)))
        plt.close()
        lst = [A,C,T,G]
        l = max([len(lst[ind]) for ind in range(len(lst))])
        r_count = [f'Round {i}']*l
        pos = [f'Position {ind+1}' for ind in range(l)]
        round_col.extend(r_count)
        position.extend(pos)
        for ind in range(len(lst)):
            if len(lst[ind]) < l:
                sub = l - len(lst[ind])
                lst[ind].extend([0]*sub)
        per_A.extend(lst[0])
        per_C.extend(lst[1])
        per_T.extend(lst[2])
        per_G.extend(lst[3])
    per_df = pd.DataFrame({'Rounds':round_col,\
                           'Positions':position,\
                               'A':per_A,\
                                   'C':per_C,\
                                       'G':per_G,\
                                           'T':per_T})  
    per_df.to_csv(os.path.join(out_path,f'{proj_name}_nucleotide_distributions.csv'),index = False)
    


def create_count_freq_table_xlsx(count_all_rounds):
    rnds = mp.get_current_rounds()
    rounds = [int(r)for r in rnds]
    outpath = mp.get_last_output_path()
    proj_name = mp.get_project_name_tmp()
    mut_num = mp.get_group_family_mut_num()

    if mut_num == 1:
        deter_fam = True
    else:
        deter_fam = False

    # if ms:
    #     proj_name = 'motif_search_' + proj_name
    if os.path.exists(os.path.join(NGS_TEMP_FOLDER, r'count_threshold.ngs')):
        thresh = int(mp.get_seq_count_threshold())

    else:
        # Set abundancy default to 200 sequences for analysis
        thresh = 200

    #con = mdb.db_connection()
    freq_all_rounds = ngst.create_freq_seq_all_rounds(count_all_rounds,rounds,thresh)
    print(freq_all_rounds.head())

    ngst.merge_counts_freqs_to_xlsx(freq_all_rounds, outpath, proj_name, deter_fam)

    # try:
    #     ngst.merge_counts_freqs_to_xlsx(con, outpath, proj_name, deter_fam)
    # except:
    #     print("FAILED: TOO MANY SEQS FOR XLSX FILE")

def write_summary_ngs(df):
    rnds = mp.get_current_rounds()
    rounds = [int(r)for r in rnds]
    out_path = mp.get_last_output_path()
    proj_name = mp.get_current_project_name()
    ngst.write_summary(os.path.join(out_path,'%s_summary.txt'%proj_name), df,rounds)



