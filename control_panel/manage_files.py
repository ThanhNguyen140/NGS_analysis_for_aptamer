# manage_file.py
"""
The "control_panel" folder contains modules that connect the user interface (GUI folder) modules with
the tool modules (tools folder).
-----------------------------------------------------------------------------------------------------
This module is for deleting temporary files in bulk. Used when program has finished completely

FUTURE TASK:
Add the ability to manage history files to keep record of all recent NGS analyses for user to reference

"""
# Needs modification and double check
import os

import tools.misc_tools as mt
from constants import *
from tools.export_tools import print_list_to_txt
from Bio import SeqIO


def delete_all_ngs_files():
    dir = NGS_TEMP_FOLDER
    if os.path.exists(dir):
        files = [f for f in os.listdir(dir) if f.endswith(".ngs")]
        for f in files:
            os.remove(os.path.join(dir, f))
    else:
        print(".ngs Files not removed")


def delete_all_tmp_files():
    dir = TEMP_FOLDER
    if os.path.exists(dir):
        files = [f for f in os.listdir(dir)] #if f.endswith(".tmp")]
        for f in files:
            os.remove(os.path.join(dir, f))
    else:
        print(".ngs Files not removed")


def set_primer_library_list():
    #print(os.getcwd())
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'primers')):
        libs = [file.replace('.xlsx', '') for file in files]
        #print(libs)
        lib_file = os.path.join(TEMP_FOLDER, r'primer_libs.tmp')
        #print(lib_file)
        print_list_to_txt(lib_file,libs)



def get_primer_library_list():
    lib_file = os.path.join(TEMP_FOLDER, r'primer_libs.tmp')

    with open(lib_file, 'r') as f:
        libs = f.read()

    fps = mt.string_to_list(libs)
    return fps



#def delete_all_ms_files():
    #dir = MOTIF_SRCH_FOLDER
    #if os.path.exists(dir):
        #files = [f for f in os.listdir(dir) if f.endswith(".ms")]
        #for f in files:
            #os.remove(os.path.join(dir, f))
    #else:
        #print(".ms files not removed")



def merge_fastq_files(fastqs):

    fastqs = mt.string_to_list(fastqs)

    fqs = [SeqIO.parse(f, "fastq") for f in fastqs]
    while True:
        for fq in fqs:
            try:
                print(next(fq).format("fastq"), end="")
            except StopIteration:
                fqs.remove(fq)
        if len(fqs) == 0:
            break