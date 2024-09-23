import sys
sys.path.append('..')
import os
import regex
import polars as pl
from Bio import SeqIO
from stringdist import levenshtein
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tools import export_tools as expt
#import tools.motif_tools as moft
import time
from sklearn.cluster import AffinityPropagation
import gzip
from collections import Counter
from PyQt5.QtCore import QObject, pyqtSignal,QThread
from PyQt5 import QtWidgets
import copy
import traceback
class open_files(QThread):
    updateSignal = pyqtSignal(int)
    updateData = pyqtSignal(pl.DataFrame)
    # Needs to be changed in GUI
    def __init__(self,files):
        super().__init__()
        self.files = files
        self.ngs_list = []
        for file in self.files: 
            if '.gz' in file: 
                with gzip.open(file,'rt') as f:
                    ngs = SeqIO.parse(f,'fastq')
            else:
                ngs = SeqIO.parse(file,'fastq')
            self.ngs_list.append(ngs)

        
    def run(self):
        '''Parameters:
        Files: list of files, in .gz or .fastq file formats
        Returns a polar dataframe with copy numbers, sequences, phred_scores if requested. '''
        sequence = []
        phred_score = []
        length = []
        i = 1
        for ngs in self.ngs_list:
            for line in ngs:
                self.updateSignal.emit(i)
                seq = str(line.seq)
                sequence.append(seq)
                length.append(len(seq))
                quality = line.letter_annotations['phred_quality']
                mean = round(sum(quality)/len(quality),2)
                phred_score.append(mean)
                i += 1
        result = pl.DataFrame({'sequence':sequence,'phred_score':phred_score,'length':length})
        self.updateData.emit(result)
#os.chdir('C://Desktop//Thanh//318_Mayer_Bahnamiri//C3AD13_split_rounds')


def remove_sequence(df,len_threshold,phred_threshold):
    '''Parameters:
        df: dataframe of sequences
        len_threshold: length threshold of sequences of interest
        phred_threshold: desired threshold of phred_score
        Returns the sequences after quality check of short sequences and phred_score'''
    df1 = df.filter((pl.col('length')>=len_threshold) & (pl.col('phred_score')>=phred_threshold))
    message = ''
    message += '{:.4%} of the sequences are shorter than {}\n'.format(len(df.filter(pl.col('length')<len_threshold))/len(df),len_threshold)
    message += '{:.4%} of the sequences have quality lower than {}\n'.format(len(df.filter(pl.col('phred_score')<phred_threshold))/len(df),phred_threshold)
    message += '{:.4%} of the sequences have been removed'.format(1-len(df1)/len(df))
    return df1, message


def complementary(seq):
    '''Returns a complementary strand'''
    dna = seq.maketrans('ATCG','TAGC')
    comp_strand = seq.translate(dna)
    return comp_strand  



def split_round(seq,primers1,primers2,rounds,random_region, mut, min_length = False, max_length = False):
    '''Parameters:
        seq : sequence of interest
        primer1: list of primers at 5'
        primer2: list of primers at 3'
        random_region: length of random region
        mut: number of mutations allowed in the forward and reverse primers
        min_length: if True, the minimum length of sequences after trimming the primers
        max_length: if True, the maximum length of sequences after trimming the primers
        If min_length and max_length are not defined, the software returns the length of random regions
        Returns a sequence without forward and reverse primers with the round that the sequence belongs to'''
    i = 0
    # Form a loop to check which round the aptamer belongs to
    while i<len(primers1):
        # Recognize the rounds by the first 6 barcodes of the sequence. No mutations allowed here
        y = regex.match(primers1[i][:6],seq)
        if y:
            # Recognize the primers at 5' for trimming. Some defined mutations are allowwed
            if regex.match('('+primers1[i]+'){s<=%d}'%mut,seq):
                seq = seq[len(primers1[i]):]
                # If min_length is defined and the sequence is shorter than the random regions
                # Remove the short sequences shorter than min_length
                # If min_length is not defined, remove sequence
                if len(seq) < random_region:
                    if min_length and len(seq) >= min_length:
                        if i > len(primers1)/2-1:
                            return complementary(seq)[::-1], rounds[int(i-len(primers1)/2)]
                        else:
                            return seq,rounds[i]
                    else:
                        return None,None
                else:
                    # Get the length of reverse primers
                    end = len(seq) - random_region
                    # Check the match between desired reverse primers and actual sequences in the the aptamers
                    # Mutations may occur at the end that shift the primers
                    # Recognize if the rev_primer region has a defined number of mutations
                    # Else, only the exact length of random regions is returned
                    pos = regex.search('('+primers2[i][:end]+'){e<=%d}'%mut,seq[random_region:])
                    if pos:
                        if max_length and max_length > random_region + pos.start():
                            seq = seq[:random_region+pos.start()]
                        elif max_length and max_length < random_region + pos.start():
                            seq = seq[:max_length]
                        elif not max_length:
                            seq = seq[:random_region]
                    else:
                        if max_length:
                            #print(primers2[i][:end])
                            #print(seq[random_region:])
                            seq = seq[:max_length]
                            #print('4: %s'%seq)
                        else:
                            seq = seq[:random_region]
                            #print('5: %s'%seq)
                if i > len(primers1)/2-1:
                    return complementary(seq)[::-1], rounds[int(i-len(primers1)/2)]
                else:
                    return seq,rounds[i]
        i += 1
    return None,None

class create_round_table(QThread):
    updateSignal = pyqtSignal(int)
    updateMaximum = pyqtSignal(int)
    updateData = pyqtSignal(pl.DataFrame)
    
    def __init__(self,df,for_primer,rev_primer, rnd, random_region, mut, min_length = False, max_length = False):
        super().__init__()
        self.df = df
        self.for_primer = for_primer
        self.rev_primer = rev_primer
        self.rnd = rnd
        self.random_region = random_region
        self.mut = mut
        self.min_length = min_length
        self.max_length = max_length
        
    def run(self):
        '''Parameters:
            seq : sequence of interest
            for_primer: forward primers
            rev_primer: reverse primers
            random_region: length of random region
            mut: number of mutations allowed in the forward and reverse primers
            min_length: if True, the minimum length of sequences after trimming the primers
            max_length: if True, the maximum length of sequences after trimming the primers
            If min_length and max_length are not defined, the software returns the length of random regions
            Returns a dataframe with count, sequence from 5' to 3' and the rounds each sequence belongs to'''
        short_df = self.df.groupby('sequence').count()
        seqs = []
        rounds = []
        if len(self.for_primer)!=len(self.rev_primer):
            raise ValueError('The number of forward primers and reverse primers are not the same!')
        primers1 = self.for_primer + self.rev_primer
        primers2 = [complementary(i)[::-1] for i in self.rev_primer]+[complementary(i)[::-1] for i in self.for_primer]
        value = len(short_df) - 1
        self.updateMaximum.emit(value)
        
        for ind,s in enumerate(short_df['sequence']):
            self.updateSignal.emit(ind)
            seq,r = split_round(s,primers1,primers2,self.rnd,self.random_region, self.mut, self.min_length, self.max_length)
            seqs.append(seq)
            rounds.append(r)
        short_df = short_df.with_columns(pl.Series(name="sequence",values=seqs))
        short_df = short_df.with_columns(pl.Series(name="rounds", values=rounds))
        self.updateData.emit(short_df)


def graph_nucleotides(df,r):
    #print(rounds, proj_name, out_path)
    A = []  # Inizialice every nucleotide list for each round
    C = []
    T = []
    G = []
    nucleotides = []
    sequences = []
    for seq,count in zip(df['sequence'],df['count_%d'%r]):
        sequences.extend([seq]*int(count))
    #length = len(max(open("%s_R%s.txt" % (proj_name, i), "r"), key=len)) - 1
    length = len(max(sequences, key=len))

    num_lines = 0
    for line in sequences:  # Split each sequence into their different nucleotides
        if len(line.strip()) == length:
            nucleotides.append(line.strip())  # Count the number of lines for each round (for percentage)
        elif len(line.strip()) < length:
            addnum = length - len(line.strip())  # Count how many nucleotides are missing
            add = ("N" * addnum)  # Add the N missing nucleotides to the sequence
            nucleotides.append(line.strip() + add)
        elif len(line.strip()) > length:
            nucleotides.append(line.strip()[0:length + 1])
        num_lines += 1
    for N in zip(*nucleotides):  # Take the nucleotides by columns to count the abundance of each nucleotide at each position
        c = Counter(N)  # "Counter" counts the abundance of each nucleotide

        for a in "ACGT":
            c[a] = (float(c[a]) * 100) / num_lines  # Calculate the percentage of the four nucleotides
        A.append(
            c["A"])  # Gather every percentage of each nucleotide for all the positions of the random region
        C.append(c["C"])
        T.append(c["T"])
        G.append(c["G"])

    ind = np.arange(length)  # Plot the percentages of each nucleotide along the random region
    width = 1
    p1 = plt.bar(ind, A, width, color='r', edgecolor='k', label = 'A')
    p2 = plt.bar(ind, T, width, bottom=A, color='#FFFF00',edgecolor='k', label = 'T')  # "Bottom" allows the stacking of the different plots (4)
    p3 = plt.bar(ind, C, width, bottom=[h + j for h, j in zip(A, T)], color='b', edgecolor='k', label='C')
    p4 = plt.bar(ind, G, width, bottom=[h + j + k for h, j, k in zip(A, T, C)], color='g', edgecolor='k', label = 'G')

    plt.yticks(np.arange(0, 101, 25),fontsize = 12)
    plt.xticks(np.arange(0, length, 5), np.arange(1, length + 1, 5), fontsize = 12)
    plt.gca().set_ylim([0, 100])
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1)).set_draggable(state=False)
    plt.xlabel("Nucleotide sequences", fontsize=14,font = 'arial',fontweight = 'bold')
    plt.ylabel("Percentage", fontsize=14, font = 'arial',fontweight = 'bold')
    return A,C,T,G
    

def plot_unique(df, rounds):
    percentages = []
   
    for r in rounds:
        df_round = df['count_%d'%r]
        total = sum(df_round)
        u = df_round[df_round==1].count()
        percentage = u/total * 100
        percentages.append(percentage)
    fig = plt.figure(figsize = (10,5))
    plt.plot(rounds,percentages, color = 'blue',marker='.',markersize = 10)
    plt.xticks(rounds, size = 12)
    plt.ylim(0,100)
    plt.yticks(np.arange(0,100,10),size = 12)
    plt.xlabel('Rounds',font = 'arial',size = 14,fontweight = 'bold')
    plt.ylabel('Unique sequences (%)',font = 'arial',size = 14, fontweight = 'bold')
    plt.title('Percentage of unique sequences', font = 'arial',size = 14, fontweight = 'bold')
        
def create_count_seq_all_rounds(df,rnds):
    '''
    Parameters:
        df: DataFrame of sequence,rounds and count
        rounds: list of all rounds
    Return a Panda DataFrame of sequence and counts for all rounds in a sorted manner. The 
    algorithm first sorted round 10, round 9,... till round 0 in decreasing orders'''
    pd_df = pd.DataFrame({'sequence':df['sequence'],'count':df['count'],'rounds':df['rounds']})
    df_list = []
    for i in rnds:
        df_round = pd_df.loc[pd_df.rounds==i]
        df_round = df_round.drop(['rounds'],axis = 1).groupby(['sequence']).sum()
        df_round.rename(columns = {'count':'count_%d'%i}, inplace = True)
        df_list.append(df_round)
    merge = df_list[0].join(df_list[1:], how = 'outer')
    merge = merge.rename_axis('sequence').reset_index()
    merge.head()
    sort_merge = merge.sort_values(by = ['count_%d'%i for i in rnds[::-1]], ascending = [False for i in range(len(rnds))])
    return sort_merge.fillna(0)

def create_freq_seq_all_rounds(df,rounds,abundancy):
    '''
    Parameters:
        df: Panda DataFrame of sequence,rounds and count
        rounds: list of all rounds
    Return a DataFrame of sequence and frquencies for all rounds'''
    
    for r in rounds:
        total = sum(df['count_%d'%r])
        df['frequency_%s'%r] = df['count_%d'%r].apply(lambda x: x/total * 100)
    return df[:abundancy]
    

def write_summary(filename, df,rounds):
    with open(filename,'w') as f:
        for ind,r in enumerate(rounds):
            df_round = df['count_%d'%r]
            total = sum(df_round)
            u = df_round[df_round==1].count()
            f.write('Round %d:\n'%r)
            f.write('Total sequences:%d \n'%total)
            f.write('Number of unique sequences: %d \n'%u)
            f.write('Number of distinct sequences:%d \n'%len(df_round[df_round > 0]))
            f.write('Percentage of unique sequences: {}%\n'.format(round(u/total * 100,2)))
            

## creates NGS_info.xlsx
def merge_counts_freqs_to_xlsx(df, out_path, project_name, deter_fam=False):
   
    if deter_fam:
        try:
            m_df = determine_families(df)#expt.sql_to_df(conn, "all_mutations", 0)
            c_df = pd.merge(m_df, df, on='sequence')
            expt.df_to_color_xlsx(c_df, os.path.join(out_path, f"{project_name}_NGS_families.xlsx"))
        except Exception as error:
                failed = QtWidgets.QMessageBox()
                failed.setText(f"{type(error)} - {error}.\n \n"
                                f"{traceback.format_exc()} \n \n"
                               "Please choose another number of enriched sequences"
                                " from count_all_rounds.csv for family analysis")
                failed.exec_()
    else:
        print('CREATING NGS_info.xlsx FILE')
        expt.df_to_color_xlsx(df, os.path.join(out_path, f"{project_name}_NGS_frequency.xlsx"))


def determine_families(df):
    '''
    

    Parameters
    ----------
    df : DataFrame containing sequences. Note: abundancy should be set because it fails if there are more than 1000
    sequences

    Returns
    -------
    cluster_df : Dataframe of sequences grouped into families. Number of families, mutations are
    annotated.

    '''
    print('CALCULATING SEQUENCE FAMILIES')
    all_seqs = np.asarray(df['sequence'])
    num_seq = all_seqs.size
    print(f'CALCULATING LEVENSHTEIN DISTANCES BETWEEN {num_seq} SEQUENCES')
    #print('NUMBER OF SEQS:', num_seq)
    
    lev_similarity = -1*np.array([[levenshtein(s1, s2) for s1 in all_seqs] for s2 in all_seqs])
    lev_similarity = lev_similarity.astype('float32')
    #print(f'{(secs/60)/60} hours')
    affprop = AffinityPropagation(affinity="precomputed", damping=.5, random_state=1)
    affprop.fit(lev_similarity)
    mut_list = []
    fam_count = 0
    print('ATTEMPTING TO CLUSTER CLOSELY RELATED SEQUENCES')
    for cluster_id in np.unique(affprop.labels_):
        exemplar = all_seqs[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(all_seqs[np.nonzero(affprop.labels_== cluster_id)])

        fam_count += 1
        if fam_count < 10:
            fc = '000'+str(fam_count)
        elif fam_count < 100:
            fc = '00'+str(fam_count)
        elif fam_count < 1000:
            fc = '0'+str(fam_count)
        else:
            fc = str(fam_count)


        fam_label = 'FAMILY_{%s}'%fc
        
        
        results = [(fam_label, levenshtein(exemplar, x), x)  for x in cluster]
        results = sorted(results, key = lambda a: a[1])
        mut_list += results
    
    cluster_df = pd.DataFrame(mut_list)
    cluster_df.columns = ['family', 'mut_num', 'sequence']
    return cluster_df

#file = 'C:\Desktop\Thanh\Testing\Burgdorf\Burgdorf.fastq'
#ngs = SeqIO.parse(file,'fastq')
#sequence = []
#phred_score = []
#length = []
#for line in ngs:
    #seq = str(line.seq)
    #sequence.append(seq)
    #length.append(len(seq))
    #quality = line.letter_annotations['phred_quality']
    #mean = round(sum(quality)/len(quality),2)
    #phred_score.append(mean)
#result = pl.DataFrame({'sequence':sequence,'phred_score':phred_score,'length':length})
#result

#for_primer = ['ATCACGGGGAGAGGAGGGAGATAGATATCAA','CGATGTGGGAGAGGAGGGAGATAGATATCAA',\
              #'TTAGGCGGGAGAGGAGGGAGATAGATATCAA','TGACCAGGGAGAGGAGGGAGATAGATATCAA',\
            #'ACAGTGGGGAGAGGAGGGAGATAGATATCAA','GCCAATGGGAGAGGAGGGAGATAGATATCAA',\
                #'CAGATCGGGAGAGGAGGGAGATAGATATCAA','ACTTGAGGGAGAGGAGGGAGATAGATATCAA',\
            #'GATCAGGGGAGAGGAGGGAGATAGATATCAA','TAGCTTGGGAGAGGAGGGAGATAGATATCAA',\
                #'GGCTACGGGAGAGGAGGGAGATAGATATCAA','CTTGTAGGGAGAGGAGGGAGATAGATATCAA']
#rev_primer = ['ATCACGGTCCTGTGGCATCCACGAAA','CGATGTGTCCTGTGGCATCCACGAAA',\
              #'TTAGGCGTCCTGTGGCATCCACGAAA','TGACCAGTCCTGTGGCATCCACGAAA',\
            #'ACAGTGGTCCTGTGGCATCCACGAAA','GCCAATGTCCTGTGGCATCCACGAAA',\
            #'CAGATCGTCCTGTGGCATCCACGAAA','ACTTGAGTCCTGTGGCATCCACGAAA',\
            #'GATCAGGTCCTGTGGCATCCACGAAA','TAGCTTGTCCTGTGGCATCCACGAAA',\
                #'GGCTACGTCCTGTGGCATCCACGAAA','CTTGTAGTCCTGTGGCATCCACGAAA']
#rnd = [1,2,3,4,5,6,7,8,9,10,11,12]
#short_df = result.groupby('sequence').count()
#seqs = []
#rounds = []
#random_region = 40
#min_length = 20
#max_length = 45
#if len(for_primer)!=len(rev_primer):
    #raise ValueError('The number of forward primers and reverse primers are not the same!')
#primers1 = for_primer + rev_primer
#primers2 = [complementary(i)[::-1] for i in rev_primer]+[complementary(i)[::-1] for i in for_primer]
#value = len(short_df) - 1

#for ind,s in enumerate(short_df['sequence']):
    #seq,r = split_round(s,primers1,primers2,rnd,random_region, 0, min_length, max_length)
    #seqs.append(seq)
    #rounds.append(r)
#short_df = short_df.with_columns(pl.Series(name="sequence",values=seqs))
#short_df = short_df.with_columns(pl.Series(name="rounds", values=rounds))

