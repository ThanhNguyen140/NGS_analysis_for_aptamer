from pathlib import Path
import os

home = str(Path.home())
apta_dir = os.getcwd()

TEMP_FOLDER = os.path.join(apta_dir, 'tmp')
TEMP_FILE = os.path.join(TEMP_FOLDER, 'temp_metadata.tmp')
CWD_DIR = apta_dir
MOTIF_SRCH_FOLDER = os.path.join(TEMP_FOLDER, 'motif_srch')
MOTIF_SRCH_DB = os.path.join(MOTIF_SRCH_FOLDER, 'motif_srch.db')
NGS_TEMP_FOLDER = os.path.join(TEMP_FOLDER, 'ngs')
ORG_SEQ = "org_seq"
RR_SEQ = "rr_seq"
SUB_SEQ = "sub_seq"
COUNT = "_count"
RAW_COLS = ['name', 'sequence','description', 'quality_score', 'file_name']
