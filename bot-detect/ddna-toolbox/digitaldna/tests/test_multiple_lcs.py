import digitaldna as ddna
import csv
from digitaldna import Verbosity
from digitaldna import SequencePlots
import pandas as pd
import numpy as np
from digitaldna.lcs import LongestCommonSubsequence
from os import listdir
from matplotlib import pyplot as plt
import time
from digitaldna import SequencePlots
​
​
def main():
​
    #from os.path import isfile, join
    savepath1 = "D:/Google Drive/Europee2019 CNR/SISP 2019/timeline utenti/non_scaricati_polarizzate/plot/"
    savepath = "D:/Google Drive/Europee2019 CNR/SISP 2019/timeline utenti/non_scaricati_polarizzate/log_plot/"
    intra_seq_path = "D:/Google Drive/Europee2019 CNR/SISP 2019/timeline utenti/non_scaricati_polarizzate/intra_seq_plot/"
    inter_seq_path = "D:/Google Drive/Europee2019 CNR/SISP 2019/timeline utenti/non_scaricati_polarizzate/inter_seq_plot/"
    mypath="D:/Google Drive/Europee2019 CNR/SISP 2019/timeline utenti/non_scaricati_polarizzate/timeline_per_id/"
​
    listafile=listdir(mypath)
    #print(listafile)
​
​
    for f in listafile:
        filepath=mypath+f
        print (filepath)
        #nome = f[3:]
        #nome = nome[:-4]
        nome = "non_scaricati_polarizzate" #assegnare nome in caso di file unico
        path_matrici = "D:/Google Drive/Europee2019 CNR/SISP 2019/timeline utenti/non_scaricati_polarizzate/matrici/"+nome+"_glcr_cache"
        df = pd.read_csv(filepath)
        est = LongestCommonSubsequence(
            out_path= path_matrici,
            overwrite=True, window=5, threshold= "auto", verbosity= Verbosity.FILE_EXTENDED)
        est.fit(df["dna"])
        y = est.fit_predict(df["dna"])
        time.sleep(5)
​
        lcslog = est.plot_LCS_log()
​
        fname = savepath + nome +'log.png'
        lcslog.savefig(fname, dpi=None)
        lcslog.close()
​
        lcs_plot = est.plot_LCS()
​
        fname1 = savepath1 + nome + '.png'
        lcs_plot.savefig(fname1, dpi=None)
        lcs_plot.close()
​
        fname2 = intra_seq_path + nome +'.png'
        plotter = SequencePlots(alphabet='b3_type')
        intra_seq = plotter.plot_intrasequence_entropy(df["dna"])
        intra_seq.savefig(fname2, dpi=None)
        intra_seq.close()
​
        fname3 = inter_seq_path + nome + '.png'
        inter_seq = plotter.plot_intersequence_entropy(df["dna"])
        inter_seq.savefig(fname3, dpi=None)
        inter_seq.close()
​
        bot_path = "D:/Google Drive/Europee2019 CNR/SISP 2019/timeline utenti/non_scaricati_polarizzate/bot_python/"
        pd.DataFrame(y).to_csv(
            bot_path + nome +"_bot.csv",
            sep=';', encoding='utf-8')
        #exit()
​
​
​
​
    #salvare plot
    #salvare y (classificazione bot)
    #tagliare "df_" e "".csv" dai file png dei plot
​
if __name__ == '__main__':
    main()