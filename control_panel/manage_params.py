
import json
import os

from tools import misc_tools as mt
from constants import *


def read_temp_metadata():
    with open(TEMP_FILE, 'r') as f:
        x = f.read()
        # print(x)
    temp_dic = json.loads(x)
    return temp_dic

def get_split():
    p_dic = get_parameters_ngs()
    return p_dic["split"]


def get_parameters_ngs():
    p_dic = read_temp_metadata()["project"][0]
    # print(p_dic)
    return p_dic

def get_rr_length():
    p_dic = get_parameters_ngs()
    rr_len = p_dic['rr_len']
    return rr_len

def get_min_length():
    p_dic = get_parameters_ngs()
    min_len = p_dic['min_len']
    return min_len

def get_max_length():
    p_dic = get_parameters_ngs()
    max_len = p_dic['min_len']
    return max_len

def get_current_rounds() -> list:
    p_dic = get_parameters_ngs()
    rounds = p_dic['rounds']
    return rounds


def get_current_files() -> list:
    params = get_parameters_ngs()
    files = params['files']
    return files


def get_current_output_path() -> str:
    params = get_parameters_ngs()
    output = params['output']
    return output


def get_current_project_name() -> str:
    params = get_parameters_ngs()
    project_name = params['project_name']
    return project_name

# This might be not needed
def get_current_db_path():
    params = get_parameters_ngs()
    db_path = os.path.join(os.path.normpath(params['output']), params['project_name'] + ".db")
    return db_path


def save_output_path(output_path):
    last_output_path = os.path.join(TEMP_FOLDER, r'last_output_path.tmp')

    with open(last_output_path, 'w') as f:
        f.write(str(output_path))


def get_last_output_path():
    last_output_path = os.path.join(TEMP_FOLDER, r'last_output_path.tmp')

    #print(last_output_path)
    if os.path.exists(last_output_path):

        with open(last_output_path, 'r') as f:
            #print('success')
            path = os.path.normpath(f.read())

    else:
        path = None

    return path


def save_last_files(files):
    last_files = os.path.join(TEMP_FOLDER, r'last_files.tmp')
    with open(last_files, 'w') as f:
        f.write(",".join(files))


def get_last_files():
    last_files = os.path.join(TEMP_FOLDER, r'last_files.tmp')
    if os.path.exists(last_files):
        with open(last_files, 'r') as f:
            files = f.read().split(',')
        #print(files)

    else:
        files = [""]
    return files


def set_forward_primers_tmp(for_prims):
    fps = ",".join(mt.string_to_list(for_prims))  ## cleans string to make sure same separation
    for_ngs = os.path.join(NGS_TEMP_FOLDER, "forward_primers.ngs")
    with open(for_ngs, 'w') as f:
        f.write(fps)


def get_forward_primers_list_tmp():
    for_ngs = os.path.join(NGS_TEMP_FOLDER, "forward_primers.ngs")

    with open(for_ngs, 'r') as f:
        primers = f.read()

    fps = mt.string_to_list(primers)
    return fps


def set_reverse_primers_tmp(rev_prims):
    rps = ",".join(mt.string_to_list(rev_prims))  ## cleans string to make sure same separation
    rev_ngs = os.path.join(NGS_TEMP_FOLDER, "reverse_primers.ngs")
    with open(rev_ngs, 'w') as f:
        f.write(rps)


def get_reverse_primers_list_tmp():
    rev_ngs = os.path.join(NGS_TEMP_FOLDER, "reverse_primers.ngs")

    with open(rev_ngs, 'r') as f:
        primers = f.read()

    rps = mt.string_to_list(primers)
    return rps

def set_split_option(splt_opt):
    splt_opt_ngs = os.path.join(NGS_TEMP_FOLDER, "split_option.ngs")
    with open(splt_opt_ngs, 'w') as f:
        f.write(splt_opt)

def get_split_option():
    splt_opt_ngs = os.path.join(NGS_TEMP_FOLDER, "split_option.ngs")
    with open(splt_opt_ngs, 'r') as f:
        splt_opt = f.read()
    
    return splt_opt



def set_project_name_tmp(proj_name):
    pro_nm_ngs = os.path.join(NGS_TEMP_FOLDER, "project_name.ngs")
    with open(pro_nm_ngs, 'w') as f:
        f.write(proj_name)


def get_project_name_tmp():
    pro_nm_ngs = os.path.join(NGS_TEMP_FOLDER, "project_name.ngs")

    with open(pro_nm_ngs, 'r') as f:
        proj_name = f.read()

    return proj_name


def set_rounds_str_tmp(rnds_str):
    rnds_str = ",".join(mt.string_to_list(rnds_str))  # cleans string
    rnds_ngs = os.path.join(NGS_TEMP_FOLDER, "rounds.ngs")
    with open(rnds_ngs, 'w') as f:
        f.write(rnds_str)


def get_rounds_str_tmp():
    rnds_ngs = os.path.join(NGS_TEMP_FOLDER, "rounds.ngs")

    with open(rnds_ngs, 'r') as f:
        rounds = f.read()

    return rounds





def get_round_table_list() -> list:
    rounds = get_current_rounds()

    tables = [f"round_{str(x)}" for x in rounds]

    return tables


def get_round_count_table_list() -> list:
    rounds = get_current_rounds()

    tables = [f"round_{str(x)}_count" for x in rounds]

    return tables


def get_motif_min_max_list() -> list:
    """
    Gets a list of motif length values ranging from min to max value (user input)
    :return: list of ints
    """


def set_motif_min_ngs(min_len):
    motif_min_len = os.path.join(NGS_TEMP_FOLDER, r'motif_min.ngs')

    if os.path.exists(motif_min_len):
        os.remove(motif_min_len)

    with open(motif_min_len, 'w') as f:
        f.write(str(min_len))


def set_motif_max_ngs(max_len):
    motif_max_len = os.path.join(NGS_TEMP_FOLDER, r'motif_max.ngs')

    if os.path.exists(motif_max_len):
        os.remove(motif_max_len)

    with open(motif_max_len, 'w') as f:
        f.write(str(max_len))


def save_primer_library_ngs(lib):
    prim_lib = os.path.join(NGS_TEMP_FOLDER, "primer_library.ngs")
    with open(prim_lib, 'w') as f:
        f.write(lib)


def get_primer_library_ngs():
    prim_lib = os.path.join(NGS_TEMP_FOLDER, "primer_library.ngs")

    with open(prim_lib, 'r') as f:
        lib = f.read()
    return lib


def save_seq_count_threshold(thresh):
    thresh_path = os.path.join(NGS_TEMP_FOLDER, "count_threshold.ngs")
    with open(thresh_path, 'w') as f:
        f.write(thresh)

def get_seq_count_threshold():
    thresh_path = os.path.join(NGS_TEMP_FOLDER, "count_threshold.ngs")
    with open(thresh_path, 'r') as f:
        thresh = f.read()

    return thresh


def save_group_family_mut_num(mut_num):
    mut_path = os.path.join(NGS_TEMP_FOLDER, "group_fam_mut_num.ngs")
    with open(mut_path, 'w') as f:
        f.write(mut_num)


def get_group_family_mut_num():
    mut_path = os.path.join(NGS_TEMP_FOLDER, "group_fam_mut_num.ngs")

    if os.path.exists(mut_path):
        with open(mut_path, 'r') as f:
            mut_num = f.read()
    else:
        mut_num = 0

    return int(mut_num)


