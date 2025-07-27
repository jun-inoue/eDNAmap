import re,os,sys,math,shutil, glob, zipfile, datetime
from socket import gethostname
from functools import reduce
from collections import OrderedDict
from utils.session_utils import load_param_from_session
from utils.session_utils import load_param_from_session
from utils.session_utils import get_session_param
from flask import session
from flask import abort
import pickle
import numpy as np
import pandas as pd
import subprocess
import time
import random

rscriptTMP = "Rscript"

#database_address = os.getenv("DATABASE_ADDRESS", "static/ASVtables/")

#filePass_English2Japanese = database_address + "Sname_Jname_1.txt"
#filePass_Sname2Cname = database_address + "Sname_Cname_15477.txt"
#def initialize_file_paths(database_address):
#    filePass_English2Japanese = os.path.join(database_address, "Sname_Jname_1.txt")
#    filePass_Sname2Cname = os.path.join(database_address, "Sname_Cname_15477.txt")
#    return filePass_English2Japanese, filePass_Sname2Cname

dir_scripts_oeDNAmap = "OEDNAMAPscripts043/"


#database_address = "ASVtables/"

widthHeightPNG_portlait_html = 'width="531" height="749"'
widthHeightPNG_landscape_html = 'width="841" height="593"'

file_grd = "ETOPO1_Ice_g_gmt4.grd"
# カレントディレクトリに存在するか確認
if os.path.exists(file_grd):
    pass
else:
    # ホームディレクトリにあるか確認（~ を展開）
    file_grd_home = os.path.expanduser(f"~/{file_grd}")
    if os.path.exists(file_grd_home):
        file_grd = file_grd_home
    else:
        raise ValueError(
            f"Error: The file '{file_grd}' was not found in the current directory or your home directory.<br>"
            f"Execution stopped.<br>"
        )

dics_cruiseName_excelFiles = OrderedDict()
dics_cruiseName_excelFiles["KH20-9AB_KH22-5_qiime2"] = ["KH20-9AB_KH22-5_qiime2.xlsx"] # 
dics_cruiseName_excelFiles["6cruisesWithoutNansei"] = ["6cruisesWithoutNansei.xlsx"] # 
dics_cruiseName_excelFiles["7crouses_withoutNansei"] = ["7crouses_withoutNansei.xlsx"] # 
dics_cruiseName_excelFiles["7crouses_withoutNansei_ASV"] = ["7crouses_withoutNansei_ASV.xlsx"] # 
dics_cruiseName_excelFiles["KH21-2_KH22-5_PMiFish"] = ["KH21-2_KH22-5_PMiFish.xlsx"] # 
dics_cruiseName_excelFiles["3cruisesPMifishWithControls"] = ["3cruisesPMifishWithControls.xlsx"] # 
dics_cruiseName_excelFiles["8cruisesPMifishwithControl"] = ["8cruisesPMifishwithControl.xlsx"] # PMifish
dics_cruiseName_excelFiles["KH20-09-KH22-05-PMifish"] = ["KH20-09-KH22-05-PMifish.xlsx"] # PMifish
dics_cruiseName_excelFiles["KS18-05"] = ["KS18-5BQ1.xlsx", "KS18-5C.xlsx"] # KS18-5BlineQ1_4_daihyou.xlsx, KS18-5_KS1815Cline_MiFish_20181115.xlsx
dics_cruiseName_excelFiles["KS18-08"] = ["KS18-08.xlsx"]  # <= KS18-08_KS19-04_KS19-07.xlsx
dics_cruiseName_excelFiles["KS19-04"] = ["KS19-04.xlsx"]  # <= KS18-08_KS19-04_KS19-07.xlsx
dics_cruiseName_excelFiles["KS19-07"] = ["KS19-07.xlsx"]  # <= KS18-08_KS19-04_KS19-07.xlsx
dics_cruiseName_excelFiles["KS19-19"] = ["KS19-19.xlsx"] # <= KS19-19_MishimaMaru.xlsx
dics_cruiseName_excelFiles["MishimaMaru"] = ["MishimaMaru.xlsx"] # <= KS19-19_MishimaMaru.xlsx
dics_cruiseName_excelFiles["KS20-13"] = ["KS20-13A.xlsx", "KS20-13B.xlsx"] # A: KS20-13_KS20-15.xlsx, B: KH20-09_KS20-13_KS20-15.xlsx
dics_cruiseName_excelFiles["KS20-13PMifish"] = ["KS20-13PMifish.xlsx"] # A: KS20-13_KS20-15.xlsx, B: KH20-09_KS20-13_KS20-15.xlsx
dics_cruiseName_excelFiles["KS20-15"] = ["KS20-15A.xlsx", "KS20-15B.xlsx"] # A: KS20-13_KS20-15.xlsx, B: KH20-09_KS20-13_KS20-15.xlsx
dics_cruiseName_excelFiles["KS22-07"] = ["KS22-7.xlsx"]
dics_cruiseName_excelFiles["KS22-11"] = ["KS22-11.xlsx"]
dics_cruiseName_excelFiles["KS22-15"] = ["KS22-15.xlsx"]

dics_cruiseName_excelFiles["KH20-09"] = ["KH20-09A.xlsx", "KH20-09B.xlsx"] # A: KH20-09.xlsx, B: KH20-09_KS20-13_KS20-15.xlsx
dics_cruiseName_excelFiles["KH20-09A"] = ["KH20-09A.xlsx"]
dics_cruiseName_excelFiles["KH20-09B"] = ["KH20-09B.xlsx"]
dics_cruiseName_excelFiles["KH20-09APMifish"] = ["KH20-09APMifish.xlsx"]
dics_cruiseName_excelFiles["KH20-09BPMifish"] = ["KH20-09BPMifish.xlsx"]
dics_cruiseName_excelFiles["KH20-09PMifish"] = ["KH20-09PMifish.xlsx"]
dics_cruiseName_excelFiles["KH20-09PMifish-withControls"] = ["KH20-09PMifish-withControls.xlsx"]
dics_cruiseName_excelFiles["KH20-9AB_qiime2"] = ["KH20-9AB_qiime2.xlsx"]

dics_cruiseName_excelFiles["KH21-2"] = ["KH21-2.xlsx"] # KH21-2_KS21-3_KS21-8.xlsx
dics_cruiseName_excelFiles["KH21-2PMiFishWithControls"] = ["KH21-2PMiFishWithControls.xlsx"] # KH21-2_KS21-3_KS21-8.xlsx

dics_cruiseName_excelFiles["KH22-01"] = ["KH22-1.xlsx"] # KH22-1_5_kanjuku_ogasawara.xlsx
dics_cruiseName_excelFiles["KH22-03"] = ["KH22-3.xlsx"] # KH22-1_5_kanjuku_ogasawara.xlsx
dics_cruiseName_excelFiles["KH22-04"] = ["KH22-4.xlsx"] # KH22-1_5_kanjuku_ogasawara.xlsx
dics_cruiseName_excelFiles["KH22-5"] = ["KH22-5.xlsx"] # KH22-1_5_kanjuku_ogasawara.xlsx
dics_cruiseName_excelFiles["KH22-05PMifish"] = ["KH22-05PMifish.xlsx"] # PMifish
dics_cruiseName_excelFiles["KH22-05PMifish-withControls"] = ["KH22-05PMifish-withControls.xlsx"] # PMifish
#dics_cruiseName_excelFiles["KH22-5_qiime2"] = ["KH22-5_qiime2.xlsx"] # Qiime2


dics_cruiseName_excelFiles["KH23-02"] = ["KH23-2.xlsx"] # KH-23-2_KS-23-2_KS-23-7_KH-23-3.xlsx
dics_cruiseName_excelFiles["KH23-03"] = ["KH23-3.xlsx"] # KH-23-2_KS-23-2_KS-23-7_KH-23-3.xlsx

dics_cruiseName_excelFiles["Ogasawara22"] = ["Ogasawara22.xlsx"] # KH22-1_5_kanjuku_ogasawara.xlsx

dics_cruiseName_excelFiles["KS21-03"] = ["KS21-3.xlsx"] # KH21-2_KS21-3_KS21-8.xlsx
dics_cruiseName_excelFiles["KS21-08"] = ["KS21-8.xlsx"] # KH21-2_KS21-3_KS21-8.xlsx
dics_cruiseName_excelFiles["KS21-11"] = ["KS21-11.xlsx"] # KS21-11_KS21-12_Otsuchi.xlsx
dics_cruiseName_excelFiles["KS21-12"] = ["KS21-12.xlsx"] # KS21-11_KS21-12_Otsuchi.xlsx
dics_cruiseName_excelFiles["KS21-24"] = ["KS21-24.xlsx"] #  KS21-24_IwateMaru_Ohtsuchi202112.xlsx 
dics_cruiseName_excelFiles["KS23-02"] = ["KS23-2.xlsx"] #  KS21-24_IwateMaru_Ohtsuchi202112.xlsx 
dics_cruiseName_excelFiles["KS23-07"] = ["KS23-7.xlsx"] #  KS21-24_IwateMaru_Ohtsuchi202112.xlsx 
dics_cruiseName_excelFiles["KS24-09"] = ["KS24-9.xlsx"] #  

dics_cruiseName_excelFiles["Otsuchi2020"] = ["Otsuchi2020.xlsx"] # KS21-11_KS21-12_Otsuchi.xlsx
dics_cruiseName_excelFiles["TEST-01"] = ["TEST-01A.xlsx","TEST-01B.xlsx"]
dics_cruiseName_excelFiles["TEST-02"] = ["TEST-02A.xlsx"]
dics_cruiseName_excelFiles["TEST-M22"] = ["TEST-M22.xlsx"]
dics_cruiseName_excelFiles["TEST-FRA"] = ["TEST-FRA-spcdat.xlsx"]

dics_cruiseName_excelFiles["Miya22"] = ["Miya22.xlsx"]
dics_cruiseName_excelFiles["Shinzato21"] = ["Shinzato21.xlsx"]
dics_cruiseName_excelFiles["Oka20"] = ["Oka20.xlsx"]
dics_cruiseName_excelFiles["Oka20PMifish"] = ["Oka20PMifish.xlsx"]
dics_cruiseName_excelFiles["Miya15"] = ["Miya15.xlsx"]
dics_cruiseName_excelFiles["Kawakami23"] = ["Kawakami23.xlsx"]
dics_cruiseName_excelFiles["Lafferty20"] = ["Lafferty20.xlsx"]
dics_cruiseName_excelFiles["Dukan24"] = ["Dukan24.xlsx"]
dics_cruiseName_excelFiles["Wu24v4"] = ["Wu24v4.xlsx"]
dics_cruiseName_excelFiles["Bessey20"] = ["Bessey20.xlsx"]
dics_cruiseName_excelFiles["Closek19"] = ["Closek19.xlsx"]
dics_cruiseName_excelFiles["Nishitsuji23"] = ["Nishitsuji23.xlsx"]
dics_cruiseName_excelFiles["Kim22"] = ["Kim22.xlsx"]


#################################################################################
####################################################
### analysis_SearchType_*
def plot_map_and_drow_figs(eachDirAddress):
    #print("#### plot_map_and_drow_figs() ####")

    list_cruiseNames = get_session_param('list_cruiseNames')
    list_dfs_cruises = get_session_param('list_dfs_cruises')
    list_dfs_cruises_stations = get_session_param('list_dfs_cruises_stations')
    list_dfs_cruises_depths = get_session_param('list_dfs_cruises_depths')

    startTime = time.time()
    #print("### Confirmation1: list_dfs_cruises ###")
    #for rec in list_dfs_cruises:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    df_envis = dict_df["environments"]
    #    print("cruiseName", cruiseName,)
    #    print("name_excelFile",name_excelFile)
    #    print("binary_or_not",binary_or_not)
    #    df_reads.to_csv(f"{eachDirAddress}8883_df_{cruiseName}_reads.csv")
    #    df_envis.to_csv(f"{eachDirAddress}88833_df_{cruiseName}_envis.csv")

    #######################################################
    # temporarily comment out
    plot_results_by_gmt(list_dfs_cruises, eachDirAddress)
    #######################################################

    elapsed_time1 = round((time.time() - startTime),1)
    #print("list_dfs_cruises 作成までにかかった時間: {0}".format(elapsed_time1) + " 秒.<br>")
    #exit()

    ################################################################
    ### Species ###############
    list_dfs_cruises_sampleIDmod = add_sampleID_cruse_depth(list_dfs_cruises)
    #print("### Confirmation2: list_dfs_cruises_sampleIDmod ###<br>")
    #for rec in list_dfs_cruises_sampleIDmod:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    df_envis = dict_df["environments"]
    #    print("cruiseName", cruiseName,)
    #    print("name_excelFile",name_excelFile)
    #    print("binary_or_not",binary_or_not)
    #    df_reads.to_csv(f"{eachDirAddress}9993_df_{cruiseName}_reads.csv")
    #    df_envis.to_csv(f"{eachDirAddress}9993_df_{cruiseName}_envis.csv")
    #    print("")
    #print("### abort analyais.py line 199 ###")
    #abort(400)

    df_4_R_percent, df_4_R_reads, df_4R_envis = make_matrix_4_R(list_dfs_cruises_sampleIDmod)
    #df_4_R_reads.to_csv(eachDirAddress + "9992_df_4_R_reads.csv")
    #df_4R_envis.to_csv(eachDirAddress + "2229_df_4R_envis.csv")
    #print("### Exit point 198 ###<br>")
    #exit()

    ##print("### Confirmation2: df_4_R_reads 1 ###<br>")
    #print("df_reads<br>")
    #for name_index_reads in df_4_R_reads.index.to_list():
    #    print("name_index_reads", name_index_reads, "<br>")
    ##for name_column_reads in df_4_R_reads.columns.to_list():
    ##    print("name_column_reads", name_column_reads, "<br>")
    ##for name_Target in df_4_R_reads['Target']:
    ##    print("name_Target", name_Target, "<br>")
    #for name_index_envis in df_4R_envis.index.to_list():
    #    print("name_index_envis", name_index_envis, "<br>")
    #exit()
    
    #####list_speices_all0detect, df_4_R_reads = delete_speciesColumns_with_all0(df_4_R_reads)
    list_speices_fewTimeDetect, df_4_R_reads = delete_speciesColumns_with_fewDetectedSites(df_4_R_reads)
    #session['list_speices_fewTimeDetect'] = pickle.dumps(list_speices_fewTimeDetect)
    #print("### Confirmation2: df_4_R_reads 2 ###<br>")
    #print("df_reads<br>")
    #for name_index in df_4_R_reads.index.to_list():
    #    print("name_index", name_index, "<br>")
    #for name_column in df_4_R_reads.columns.to_list():
    #    print("name_column", name_column, "<br>")
    #for name_Target in df_4_R_reads['Target']:
    #    print("name_Target", name_Target, "<br>")
    #exit()


    list_sampleID_all0, df_4_R_reads = delete_sampleIDlines_with_all0(df_4_R_reads)
    session['list_sampleID_all0'] = pickle.dumps(list_sampleID_all0)

    #df_4_R_percent.to_csv(eachDirAddress + "200_communityData4R_percent.csv")
    #print("df_4_R_reads.index.to_list()", df_4_R_reads.index.to_list(), "<br>")
    df_4_R_reads.to_csv(eachDirAddress + "200_communityData4R.csv")

    ### read と envis sheet の行とその行数を揃える。
    #df_4_R_reads.to_csv(eachDirAddress + "900_df_4_R_reads.csv")
    #df_4R_envis.to_csv(eachDirAddress + "900_df_4_R_envis.csv")
    df_4R_envis = arrange_index(df_4_R_reads, df_4R_envis)
    #df_4R_envis.to_csv(eachDirAddress + "900_df_4_R_envis1.csv")
    #print("### Exit point 225 ###<br>")
    #exit()
    df_4R_envis.to_csv(eachDirAddress + "200_environmentData4R.csv")

    if len(df_4_R_reads.index) > 2:
        pheatmap_R(eachDirAddress, "200_communityData4R.csv", "210_pheatmap")
        nMDS_R("200_communityData4R.csv", eachDirAddress, "220_nMDS")
        hclust_R("200_communityData4R.csv", eachDirAddress, "230_hclust")


    ################################################################
    ### location  ###############
    #print("### Confirmation location: list_dfs_cruises_stations ###<br>")
    #for rec in list_dfs_cruises_stations:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    df_envis = dict_df["environments"]
    #    print("cruiseName",cruiseName,"<br>")
    #    print("name_excelFile",name_excelFile,"<br>")
    #    print("binary_or_not",binary_or_not,"<br><br>")
    #    df_4_R_percent.to_csv(eachDirAddress + "910_communityData4R.csv")

    list_dfs_cruises_stationMod = add_station_cruise(list_dfs_cruises_stations)
    #print("### Confirmation location: list_dfs_cruises_stationMod ###<br>")
    #for rec in list_dfs_cruises_stationMod:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    df_envis = dict_df["environments"]
    #    print("cruiseName",cruiseName,"<br>")
    #    print("name_excelFile",name_excelFile,"<br>")
    #    print("binary_or_not",binary_or_not,"<br><br>")
    #    df_4_R_percent.to_csv(eachDirAddress + "920_communityData4R.csv")
    #    
    #exit()

    df_4_R_percent_station, df_4_R_reads_station, df_4_R_envis_station = make_matrix_4_R(list_dfs_cruises_stationMod)
    list_speices_fewTimeDetect_station, df_4_R_reads_station = delete_speciesColumns_with_fewDetectedSites(df_4_R_reads_station)
    list_sampleID_all0_station, df_4_R_reads_station = delete_sampleIDlines_with_all0(df_4_R_reads_station)

    # index でソート
    df_4_R_reads_station_sorted = df_4_R_reads_station.sort_index()

    #df_4_R_reads_station.to_csv(eachDirAddress + "200_communityData4R_station.csv")
    df_4_R_reads_station_sorted.to_csv(eachDirAddress + "200_communityData4R_station.csv")

    #####

    if len(df_4_R_reads_station.index) > 2:
        pheatmap_R(eachDirAddress, "200_communityData4R_station.csv", "210_pheatmap_station")
        nMDS_R("200_communityData4R_station.csv", eachDirAddress, "220_nMDS_station")
        hclust_R("200_communityData4R_station.csv", eachDirAddress, "230_hclust_station")

    ################################################################
    ########### Depth
    
    if len(list_cruiseNames) <  2:
        df_4_R_percent_depth, df_4_R_reads_depth = make_matrix_depth_4_R(list_dfs_cruises_depths)
        df_4_R_reads_depth.to_csv(eachDirAddress + "200_communityData4R_depth.csv")
        if len(df_4_R_reads_depth.index) > 2:
            pheatmap_depth_R("200_communityData4R_depth.csv", eachDirAddress, "210_pheatmap_depth")

    #makeList_species_numSeq(outFileName = "400_species_detectedFrequencies.csv")


def arrange_index(df_R_read, df_R_envi):
    #print("#### arrange_index() ####<br>")
    #df_R_read.to_csv(eachDirAddress + "999_df_R_read.csv")
    #df_R_envi.to_csv(eachDirAddress + "999_df_R_envi.csv")

    # Create a new DataFrame for df_R_envi_mod
    df_R_envi_mod = df_R_envi.copy()

    # Initialize an empty DataFrame to store the matching rows
    df_R_envi_mod = df_R_envi_mod[0:0]  # 改訂箇所1: 空のDataFrameに初期化

    # Replace the index of df_R_read with the index of df_R_envi
    for index_read in df_R_read.index:
        # Find the matching read index that contains the keyword from index_envi
        #print("index_read", index_read, "<br>")
        dic_matching_read_index = {}
        for index_envi in df_R_envi.index:
            index_envi_tmp = "_" + index_envi + "_"
            #print("index_envi_tmp", index_envi_tmp, "<br>")
            #if index_envi_tmp in index_read:
            if re.search(index_envi_tmp, index_read):
                dic_matching_read_index[index_read] = index_envi
        if len(dic_matching_read_index) == 0:
            print(f"Error: cannot find matching for {index_read} in the location sheet.")
            exit()
        elif len(dic_matching_read_index) > 1:
            print(f"Error: more than one matching for {index_read} in location sheet.")
            exit()
        else:
            # Append the matching row to df_R_envi_mod
            df_R_envi_mod = pd.concat([df_R_envi_mod, df_R_envi.loc[[dic_matching_read_index[index_read]]]])   # 改訂箇所2: 対応する行を追加
            # Rename the index in df_R_envi_mod
            df_R_envi_mod.rename(index={dic_matching_read_index[index_read]: index_read}, inplace=True)  # 改訂箇所3: インデックスの名前を変更

    #print("### Exit point 339 ###<br>")
    #exit()
    return df_R_envi_mod


def delete_sampleIDlines_with_all0(df_4_R_reads):
    #print("### delete_sampleIDlines_with_all0() ###<br>")
    #print("df_4_R_reads.to_string()", df_4_R_reads.to_string(), "<br>")
    #print("### delete_speciesColumns_with_all0() ###<br>")

    # df_4_R_reads を確認
    #print("df_4_R_reads.columns.to_list()<br>")
    #print(df_4_R_reads.columns.to_list(), "<br>")
    #for index, row in df_4_R_reads.iterrows():
    #    print(f"Index: {index}<br>")
    #    print("row.values", row.values, "<br>")
    #    print("<br>")
    #print("<br>")

    # 全ての列が 0 の行をフィルタリング
    df_reads_all0 = df_4_R_reads[(df_4_R_reads == 0).all(axis=1)]

    # 全て 0 であった行の index をリストに格納
    list_sampleID_all0 = df_reads_all0.index.tolist()
    #print("list_sampleID_all0", list_sampleID_all0, "<br>")
    #exit()
    ## df_reasw_all0 を確認
    #print("df_reasw_all0<br>")
    #for index, row in df_reads_all0.iterrows():
    #    print(f"Index: {index}<br>")
    #    print("row.values", row.values, "<br>")
    #    print("<br>")
    #print("<br>")
    #exit()

    # zero_rows_index の行を削除して、新しいデータフレームに格納
    df_4_R_reads_dropped = df_4_R_reads.drop(index=list_sampleID_all0)

    ## df_4_R_reads_dropped を確認
    #print("df_4_R_reads_dropped<br>")
    #for index, row in df_4_R_reads_dropped.iterrows():
    #    print(f"Index: {index}<br>")
    #    print("row.values", row.values, "<br>")
    #    print("<br>")
    #print("<br>")
    #exit()
    
    if len(list_sampleID_all0) > 0:
        return list_sampleID_all0, df_4_R_reads_dropped
    else:
        return list_sampleID_all0, df_4_R_reads


def delete_speciesColumns_with_fewDetectedSites(df_4_R_reads):
    #print("### delete_speciesColumns_with_fewDetectedSites() ###<br>")
    #print("df_4_R_reads.to_string()", df_4_R_reads.to_string(), "<br>")
    #print("df_4_R_reads.columns", df_4_R_reads.columns, "<br>")
    #print("df_4_R_reads.index", df_4_R_reads.index, "<br>")
    #print("### delete_speciesColumns_with_all0() ###<br>")
    
    ASV_comparison_criteria = get_session_param('ASV_comparison_criteria')

    ### df_4_R_reads を確認
    #print("### Confirmation: df_4_R_reads.columns.to_list() 1 ###<br>")
    #print("df_4_R_reads.columns.to_list()", df_4_R_reads.columns.to_list(), "<br>")
    ##print("df_4_R_reads.shape[1]", df_4_R_reads.shape[1], "<br>")
    #for index, row in df_4_R_reads.iterrows():
    #    print(f"Index: {index}<br>")
    #    print("row.values", row.values, "<br>")
    #    print("<br>")
    #print("<br>")
    #exit()

    # ASV_comparison_criteria に満たない検出回数の種をリスト
    series_columns_filtered = (df_4_R_reads.loc[:, df_4_R_reads.columns != "Target"] != 0).sum(axis=0) < int(ASV_comparison_criteria)
    # 1. df_4_R_reads.loc[:, df_4_R_reads.columns != "Target"]:
    #    df_4_R_reads データフレームの "Target" 列以外のすべての列を選択します。
    # 2. != 0:
    #    各セルが 0 でないかどうかをチェックします。0 でない場合は True、0 の場合は False になります。
    # 3. .sum(axis=0):
    #    各列に対して、True の数を合計します。つまり、各列で 0 でない値の数をカウントします。
    # 4. < int(ASV_comparison_criteria):
    #    各列の 0 でない値の数が ASV_comparison_criteria より小さいかどうかをチェックします。ASV_comparison_criteria は 2 に設定されています。
    # この結果、series_columns_filtered には、0 でない値の数が ASV_comparison_criteria より少ない列が True としてマークされたシリーズが格納されます。

    list_speices_fewTimeDetect = series_columns_filtered[series_columns_filtered].index.to_list()
    # 1. series_columns_filtered[series_columns_filtered]:
    # series_columns_filtered は Pandas のシリーズであり、各列が True または False でマークされています。この部分は、True とマークされた列のみをフィルタリングします。
    #print("list_speices_fewTimeDetect", list_speices_fewTimeDetect, "<br>")
    # 2. .index:
    # フィルタリングされたシリーズのインデックス（列名）を取得します。
    
    df_4_R_reads_dropped = df_4_R_reads.drop(columns=list_speices_fewTimeDetect)
    #print("df_4_R_reads_dropped", df_4_R_reads_dropped, "<br>")
    #if df_4_R_reads_dropped.shape[1] < 2:
    #    print(f"Error: After removing the species using the following parameters, the number of species to be analyzed became insufficient.　<br>")
    #    print(f"ASV comparison criteria: {ASV_comparison_criteria} sampling points. <br>")
    #    exit()
    if df_4_R_reads_dropped.shape[1] < 2:
        raise ValueError(
            f"Error: After removing species based on the ASV comparison criteria, the number of species is insufficient.<br>"
            f"ASV comparison criteria: {ASV_comparison_criteria} sampling points.<br>"
        )


    ### df_4_R_reads を確認
    #print("### Confirmation: df_4_R_reads.columns.to_list() 2 ###<br>")
    #print("df_4_R_reads_dropped.columns.to_list()", df_4_R_reads_dropped.columns.to_list(), "<br>")
    ##print("df_4_R_reads_dropped.shape[1]", df_4_R_reads_dropped.shape[1], "<br>")
    #for index, row in df_4_R_reads_dropped.iterrows():
    #    print(f"Index: {index}<br>")
    #    print("row.values", row.values, "<br>")
    #    print("<br>")
    #print("<br>")
    #exit()

    if len(list_speices_fewTimeDetect) > 0:
        return list_speices_fewTimeDetect, df_4_R_reads_dropped
    else:
        return list_speices_fewTimeDetect, df_4_R_reads


def delete_speciesColumns_with_all0(df_4_R_reads):

    #print("df_4_R_reads.to_string()", df_4_R_reads.to_string(), "<br>")
    #print("### delete_speciesColumns_with_all0() ###<br>")
    list_speices_all0detect = []
    # 各列をチェックして、0 だけからなる列の名前を取得
    for col in df_4_R_reads.columns:
        if df_4_R_reads[col].dtype != 'object' and (df_4_R_reads[col] == 0).all():
            list_speices_all0detect.append(col)

    #print("len(list_speices_all0detect)", len(list_speices_all0detect), "<br>")
    if len(list_speices_all0detect) > 0:
        # 0 だけからなる列をデータフレームから削除
        df_4_R_reads_new = df_4_R_reads.drop(columns=list_speices_all0detect)
        return list_speices_all0detect, df_4_R_reads_new
    else:
        return list_speices_all0detect, df_4_R_reads


def make_center_range(file_path):
    df = pd.read_csv(file_path, sep='\t', header=None, names=['Longitude', 'Latitude', 'station'])
    
    # Latitude 列から数値以外の値を除外する
    df['Latitude'] = pd.to_numeric(df['Latitude'])
    df['Longitude'] = pd.to_numeric(df['Longitude'])
    # Latitude 列と Longitude 列を数値に変換する
    df['Latitude'] = pd.to_numeric(df['Latitude'])
    df['Longitude'] = pd.to_numeric(df['Longitude'])
    # 値が 0 の行を除外する
    df = df[(df['Latitude'] != 0) & (df['Longitude'] != 0)]
    
    center_longitude = calculate_center_dist(df)
    center_latitude = (df['Latitude'].max() + df['Latitude'].min()) / 2
    range_longitude_deg = calculate_range_longitude(df)
    range_latitude_deg = calculate_range_latitude(df)
    max_latitude = df['Latitude'].max()
    min_latitude = df['Latitude'].min()

    longitudes = df['Longitude'].apply(lambda x: x if x >= 0 else x + 360)
    max_longitude = longitudes.max()
    min_longitude = longitudes.min()
    
    return round(center_latitude, 2), round(center_longitude, 2), round(range_latitude_deg, 2), round(range_longitude_deg, 2),round(max_latitude, 2), round(max_longitude, 2), round(min_latitude, 2), round(min_longitude, 2)


def make_matrix_4_R(list_dfs_fn):
    #print("### make_matrix_4_R() ###<br>")
    df_4_R_reads = ""
    #print("len(list_dfs_cruises)", len(list_dfs_cruises), "<br>")

    df_reads_merged = ""
    df_environments_merged = ""
    #print("### Confirmation list_dfs_fn ###<br>")
    #for rec in list_dfs_fn:
    #    cruiseName = rec[0]
    #    binary_or_not = rec[3]
    #    print("cruiseName", cruiseName, "<br>")
    #    print("binary_or_not", binary_or_not, "<br>")
    #exit()
    df_reads_merged, df_environments_merged = merge_severalCruseSeveralDFs_to_1df(list_dfs_fn)

    df_4_R_reads = df_reads_merged.transpose()
    df_4_R_percent = df_4_R_reads.apply(lambda x: (x / x.sum() * 100).round(2))
    return df_4_R_percent, df_4_R_reads, df_environments_merged

def make_matrix_depth_4_R(list_dfs_depth_fn):
    #print("### make_matrix_depth_4_R() ###<br>")
    #exit()
    df_4_R_reads = ""
    #print("len(list_dfs_cruises)", len(list_dfs_cruises), "<br>")

    df_reads_merged = ""
    df_environments_merged = ""
    #print("### Confirmation list_dfs_depth_fn ###<br>")
    #for rec in list_dfs_depth_fn:
    #    cruiseName = rec[0]
    #    binary_or_not = rec[3]
    #    print("cruiseName", cruiseName, "<br>")
    #    print("binary_or_not", binary_or_not, "<br>")
    #exit()
    df_reads_merged, df_environments_merged = merge_severalCruseSeveralDFs_to_1df_depth(list_dfs_depth_fn)

    df_4_R_reads = df_reads_merged.transpose()
    df_4_R_reads.index.name = "Depth"
    df_4_R_percent = df_4_R_reads.apply(lambda x: (x / x.sum() * 100).round(2))
    
    return df_4_R_percent, df_4_R_reads


def check_dfs(list_dfs_cruises):
    #print("### check_dfs() ###<br>")
    #print("input_file_userDB.filename", input_file_userDB.filename, "<br>")
    for rec in list_dfs_cruises:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dic_df = rec[2]
        #df_reads = dic_df["reads"]
        df_reads = dic_df[list(dic_df.keys())[0]]
        df_envis = dic_df[list(dic_df.keys())[1]]
        #print("cruiseName", cruiseName, "<br>")
        #print("name_excelFile", name_excelFile, "<br>")

        #print("cruiseName", cruiseName, "<br>") 
        #print("name_excelFile", name_excelFile, "<br>")
        #print("dic_df", dic_df, "<br>")
        #print("<br>")

        #if not "reads" in dic_df:
        #    print("check_excelFile(): sheet name, reads, is not found in ", fileName_excel_fn, "file.")
        #    exit()
        #if not "environments" in dic_df:
        #    print("check_excelFile(): sheet name, environments, is not found in ", fileName_excel_fn, "file.")
        #    exit()
        
        ### Environmental sheet
        list_names_column = ["Cruise", "Station", "Latitude", "Longitude", "Depth", "Day"]
        #print("df_envis.columns", df_envis.columns, "<br>")
        #print("df_envis.index.name", df_envis.index.name, "<br>")
        if not df_envis.index.name == "SampleID":
            if cruiseName == "User-xlsx":
                print('Error: The column name, "SampleID," is not found in the environmental sheet of your uploaded excel file.<br>')
            elif cruiseName == "User-csv" or cruiseName == "User-txt":
                print('Error1 in the code: The dummy environment has a problem.<br>')
            else:
                print('Error: The column name, "SampleID," is not found in the environmental sheet of {name_excelFile}.<br>')
            exit()
        for name_column in list_names_column:
            if not name_column in list(df_envis.columns):
                if cruiseName.startswith("User-"):
                    print(f'Error: The column name, {name_column}, is not found in the environmental sheet of your uploaded excel file.<br>')
                elif cruiseName == "User-csv" or cruiseName == "User-txt":
                    print(f'Error in the code 2: The dummy environment have a problem.<br>')
                else:
                    print(f'Error: The column name, {name_column}, is not found in the environmental sheet of {name_excelFile}.<br>')
                exit()
        
        for elementA in df_envis.index.tolist():
            if elementA not in df_reads.columns.tolist():
                if cruiseName.startswith("User-"):
                    print(f"Error1092 in your uploaded {input_file_userDB.filename} file.<br>")
                    print(f"The column names of read sheet and the SampleID column of environment sheet should be same.<br>")
                    print(f"{elementA} is not found in the read-sheet column-name.<br>")
                else:
                    print(f"Error1094: In {name_excelFile}, {elementA} is not found in the read-sheet sampleID-column.<br>")
                exit()

        ### Reed sheet
        #print("df_reads.columns", df_reads.columns, "<br>")
        #print("df_reads.index.name", df_reads.index.name, "<br>")
        #print("df_reads.index", df_reads.index, "<br>")

        names_column_reads = list(df_reads.columns)
        #print("names_column_reads", names_column_reads, "<br>")
        if names_column_reads[-1] != "Target":
            if cruiseName == "User-xlsx":
                print('Error1134 in your uploaded file, ', input_file_userDB.filename, ': The reads sheet should end with the "Target" column. <br>')
            else:
                print('Error1136 in ', name_excelFile, ': The reads sheet should end with the "Target" column. <br>')
            exit()
        
        #print("111df_reads.index", df_reads.index, "<br>")
        #print("111df_reads.iloc[:, 0]", df_reads.iloc[:, 0], "<br>")
        #print("111df_reads.columns", df_reads.columns, "<br>")
        #exit()
        if not pd.api.types.is_numeric_dtype(df_reads.iloc[:, 0]):
            if cruiseName == "User-xlsx" or cruiseName == "User-csv":
                print(f"Error: The first column should be the read numbers in the read sheet (1st sheet) of your uploaded excel file.<br>")
                exit()
            elif cruiseName == "User-txt":
                print(f"Error1003 in the first read column named of the uploaded txt file.<br>")
                exit()
            else:
                print(f"Error in the preinstalled excel file: The first column should be ASV or OTU ids in the {name_excelFile} reads sheet.<br>")
                exit()

        for elementA in df_reads.columns.tolist():
            #print("elementA", elementA, "<br>")
            if elementA == "Target": break
            if elementA not in df_envis.index.tolist():
                if cruiseName.startswith("User-"):
                    print(f"Error1117: In your uploaded {input_file_userDB.filename} file, {elementA} is not found in the environment-sheet sampleID-column.<br>")
                else:
                    print(f"Error1117: In {name_excelFile}, {elementA} is not found in the environment-sheet sampleID-column.<br>")
                exit()


def add_binaruy_or_not(list_dfs_cruises):
    #print("### add_binaruy_or_not() ###<br>")
    list_dfs_cruises_excelFiles_mod = []
    for rec in list_dfs_cruises:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dic_df = rec[2]
        #df_reads = dic_df["reads"]
        df_reads = dic_df[list(dic_df.keys())[0]]
        df_envis = dic_df[list(dic_df.keys())[1]]
        
        binary_or_not = check_binary_userfile_columns(df_reads)
        #print("cruiseName", cruiseName, "<br>")
        #print("binary_or_not:", binary_or_not, "<br>")

        list_dfs_cruises_excelFiles_mod.append([cruiseName, name_excelFile, dic_df, binary_or_not])

    return list_dfs_cruises_excelFiles_mod


def check_binary_userfile_columns(df_read_fn):
    #print("### check_binary_userfile_columns() ####<br>")
    # Target 列を除外したデータフレームを作成
    df_numeric = df_read_fn.drop(columns=['Target'])
    #print("df_read_fn", df_read_fn, "<br>")
    #exit()
    # index を無視して、数値コラムをチェック
    binary_columns = df_numeric.apply(lambda col: col.isin([0, 1]).all(), axis=0)
    
    #if binary_columns.all():
    if binary_columns.all() or (df_numeric == 1).all().all():
        return "binary"
    else:
        return "not-binary"


def change_underscore2datash(names):
    newNames = []
    for name in names:
        name2 = re.sub("_", "-", name)
        newNames.append(name2)
    return newNames


#def sum_num_of_allReads(numbers_of_reads_FN):
#    #print("numbers_of_reads_FN", numbers_of_reads_FN)
#    nums_int = list(map(int, numbers_of_reads_FN))
#    #print("nums_int",nums_int)
#    #exit()
#    sum_all = (sum(nums_int))
#    return sum_all


def calculate_percent(numbers_of_reads_FN):
    #if readNumber_CompareSpeciesList == "logarithm_transformation":
    #    numbers_of_reads_FN = list(map(float, numbers_of_reads_FN))
    #else:
    #    numbers_of_reads_FN = list(map(int, numbers_of_reads_FN))
    numbers_of_reads_FN = list(map(int, numbers_of_reads_FN))
    sum_all = (sum(numbers_of_reads_FN))
    nums_percent = []
    for num in numbers_of_reads_FN:
        num = int(num)/sum_all * 100
        nums_percent.append(round(num, 4))
    return nums_percent


def make_dic_2Jnameor2Cname(filePass):
    dictionary_scName2 = {}

    fTMP = open(filePass)
    lines = list(fTMP)
    fTMP.close()
    
    for line in lines:
        scName, trname = line.split("\t")
        dictionary_scName2[scName] = trname
    
    return dictionary_scName2



#def sort_calculatePercents_of_reads_for_one_sampleID(sampleID_fn, df_reads):
#    #print("sampleID_fn", sampleID_fn,"<br>")
#    #print("df_reads", df_reads,"<br>")
#    sort_columnName = sampleID_fn
#    # https://note.nkmk.me/python-pandas-sort-values-sort-index/
#    df_reads_sorted = df_reads.sort_values([sampleID_fn], ascending=[False])
#    #print("df_reads_sorted", df_reads_sorted,"<br>")
#    #exit()
#
#    names_species = list(df_reads_sorted["Target"])
#    names_species = change_underscore2datash(names_species)
#
#    numbers_of_reads = list(df_reads_sorted[sampleID_fn])
#    #num_allReads = sum_num_of_allReads(numbers_of_reads)
#    percents_of_reads = calculate_percent(numbers_of_reads)
#    
#    OTUs_ID = names_species = list(df_reads_sorted.index)
#
#    return OTUs_ID, names_species, numbers_of_reads, percents_of_reads


def sort_reads_for_one_sampleID(sampleID_fn, df_reads):
    #print("sampleID_fn", sampleID_fn,"<br>")
    #print("df_reads", df_reads,"<br>")
    # https://note.nkmk.me/python-pandas-sort-values-sort-index/
    df_reads_sorted = df_reads.sort_values([sampleID_fn], ascending=[False])
    #print("df_reads_sorted", df_reads_sorted,"<br>")
    #exit()

    names_species = list(df_reads_sorted["Target"])
    #names_species = change_underscore2datash(names_species)

    numbers_of_reads = list(df_reads_sorted[sampleID_fn])
    #num_allReads = sum_num_of_allReads(numbers_of_reads)
    #percents_of_reads = calculate_percent(numbers_of_reads)
    
    OTUs_ID = list(df_reads_sorted.index)

    return OTUs_ID, names_species, numbers_of_reads

def make_df_envis(cruiseName, list_sampleIDs_reads_fn):

    list_name_column_envis = ['Cruise', 'Station', 'Latitude', 'Longitude', 'Depth', 'Day']
    # SampleIDと NONE 列を持つ辞書を作成
    data_envis = {'SampleID': list_sampleIDs_reads_fn}
    for column in list_name_column_envis:
        if column == "Cruise":
            data_envis[column] = [cruiseName] * len(list_sampleIDs_reads_fn)
        else:
            data_envis[column] = ['NONE'] * len(list_sampleIDs_reads_fn)

    # データフレームを作成
    df_envis_fn = pd.DataFrame(data_envis)
    df_envis_fn.set_index('SampleID', inplace=True)

    return df_envis_fn


def check_and_read_excel_sheets(file_path, index_col=0):
    if os.path.exists(file_path):
        try:
            df_sheet_each = pd.read_excel(file_path, sheet_name=None, index_col=index_col)
            df_sheet_each = OrderedDict(df_sheet_each)  # OrderedDictに変換
            #print("ファイルの読み込みに成功しました。")
            return df_sheet_each
        except Exception as e:
            print(f"Error1: Cannot find {input_file_userDB.filename}.<br>")
            exit()
            return None
    else:
        print(f"Error2: Cannot find {input_file_userDB.filename}.<br>")
        exit()
        return None


def check_and_read_excel_sheets(file_path, index_col=0):
    if os.path.exists(file_path):
        try:
            df_sheet_each = pd.read_excel(file_path, sheet_name=None, index_col=index_col)
            df_sheet_each = OrderedDict(df_sheet_each)  # OrderedDictに変換
            #print("ファイルの読み込みに成功しました。")
            return df_sheet_each
        except Exception as e:
            print(f"Error1: Cannot find {file_path}.<br>")
            exit()
            return None
    else:
        print(f"Error2: Cannot find {file_path}.<br>")
        exit()
        return None


def read_file_content(file_path):
    #print("### read_file_content() ###<br>")
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            
        if not content:
            print(f"Cannot find your txt file, {input_file_userDB.filename}.<br>")
            exit()
        return content
    except IOError:
        print(f"Error in txt: Cannot find txt file, {input_file_userDB.filename}.<br>")
        exit()
        return None

def get_environments_reads_as_df(eachDirAddress, list_cruiseNames_fn, database_address):
    #print("### get_environments_reads_as_df() ###<br>")

    ASV_comparison_criteria = get_session_param('ASV_comparison_criteria')


    list_dfs_cruises_fn = []

    for cruiseName in list_cruiseNames_fn:
        #print("### list_cruiseNames_fn ###<br>")
        #print("cruiseName", cruiseName, "<br>")
        #print("eachDirAddress", eachDirAddress, "<br>")

        if cruiseName == "User-xlsx":
            #print("cruiseName User-xlsx<br>")
            if not os.path.exists(eachDirAddress + "000_user.xlsx"):
                print(f'Error: catnnot find {eachDirAddress}000_user.xlsx.<br>')
                exit()

            fileName_excel = "000_user.xlsx"

            #df_sheet_each = pd.read_excel(eachDirAddress + fileName_excel, sheet_name=None, index_col=0)
            df_sheet_each = check_and_read_excel_sheets(eachDirAddress + fileName_excel)
            
            #fileName_excel = "000_user-binary.xlsx"

            #df_reads = df_sheet_each[list(df_sheet_each.keys())[0]]
            # 1枚目のシートをデータフレームに格納し、インデックスをリセットする
            df_reads = df_sheet_each[list(df_sheet_each.keys())[0]].reset_index()
            #print("df_reads.columns", df_reads.columns, "<br>")
            #print("df_reads.iloc[:, 0]", df_reads.iloc[:, 0], "<br>")
            #print("df_reads.iloc[:, 1]", df_reads.iloc[:, 1], "<br>")
            if df_reads.iloc[:, 0].isnull().all():
                print(f"Error: The first column of your uploaded {input_file_userDB.filename} file is empty.<br>")
                exit()
            #exit()
            df_reads.index.name = '#USERXLSX'
            df_envis = df_sheet_each[list(df_sheet_each.keys())[1]]
            df_reads.to_csv(eachDirAddress + "002_df_reads_added.xlsx.csv")
            df_envis.to_csv(eachDirAddress + "002_df_envis_added.xlsx.csv")
            #exit()

            df_sheet_each = OrderedDict()
            df_sheet_each["reads"] = df_reads
            df_sheet_each["environments"] = df_envis

            list_dfs_cruises_fn.append([cruiseName, fileName_excel, df_sheet_each])

        elif cruiseName == "User-csv":
            if not os.path.exists(eachDirAddress + "000_user.csv"):
                print(f'Error: catnnot find {eachDirAddress}000_user.csv.<br>')
                exit()
            fileName_excel = "000_user.csv"

            #df_reads = pd.read_csv(eachDirAddress + fileName_excel)
            df_reads = check_and_read_csv(eachDirAddress + fileName_excel)

            df_reads.index.name = '#USERCSV'
            #print("df_reads.index", df_reads.index, "<br>")
            
            df_envis = pd.DataFrame()
            list_sampleIDs_reads = df_reads.columns.to_list()[:-1]  ## Deleting Target
            df_envis = make_df_envis(cruiseName, list_sampleIDs_reads)

            df_sheet_each = OrderedDict()
            df_sheet_each["reads"] = df_reads
            df_sheet_each["environments"] = df_envis

            list_dfs_cruises_fn.append([cruiseName, fileName_excel, df_sheet_each])

        elif cruiseName == "User-txt":
            if not os.path.exists(eachDirAddress + "000_user.txt"):
                print(f'Error: catnnot find {eachDirAddress}000_user.txt.<br>')
                exit()
            fileName_excel = "000_user.txt"
            
            stripped_content = []
            #with open(eachDirAddress + "000_user.txt", 'r') as file:
            #    content = file.readlines()
            content = read_file_content(eachDirAddress + "000_user.txt")
            for line in content:
                stripped_content.append(line.strip())

            df_reads = pd.DataFrame(stripped_content, columns=['Target'])
            df_reads.insert(0, 'User1', 9999)
            
            df_reads.index.name = '#USERTXT'
            #print("df_reads.index", df_reads.index, "<br>")
            #print("df_reads.columns", df_reads.columns, "<br>")
            #print("### Endpoint sss ###<br>")
            #exit()
            
            df_envis = pd.DataFrame()
            list_sampleIDs_reads = df_reads.columns.to_list()[:-1]  ## Deleting Target
            df_envis = make_df_envis(cruiseName, list_sampleIDs_reads)

            df_sheet_each = OrderedDict()
            df_sheet_each["reads"] = df_reads
            df_sheet_each["environments"] = df_envis

            list_dfs_cruises_fn.append([cruiseName, fileName_excel, df_sheet_each])

        elif not cruiseName in dics_cruiseName_excelFiles:
            print("Error: cruiseName", cruiseName, " was NOT found in OrderedDict, dics_cruiseName_excelFiles<br>")
            exit()

        else:
            list_excelFiles = dics_cruiseName_excelFiles[cruiseName]
    
            for fileName_excel in list_excelFiles:
                #print("fileName_excel", fileName_excel, "<br>")
                df_sheet_each = ""
                if os.path.isfile(database_address + fileName_excel):
                    df_sheet_each = pd.read_excel(database_address + fileName_excel, sheet_name=None, index_col=0)
                else:
                    file_path = os.path.join(database_address, fileName_excel)
                    if not os.path.isfile(file_path):
                        raise FileNotFoundError(
                            f"Required file '{fileName_excel}' not found in '{database_address}'.\n"
                            f"Please ensure the file exists and is accessible."
                        )
                    else:
                        raise ValueError(
                            f"Error: After removing species based on the ASV comparison criteria, the number of species is insufficient.\n"
                            f"ASV comparison criteria: {ASV_comparison_criteria} sampling points.\n"
                        )


                #df_reads = df_sheet_each[list(df_sheet_each.keys())[0]]
                #df_envis = df_sheet_each[list(df_sheet_each.keys())[1]]
                #df_reads.to_csv(f"{eachDirAddress}111_Bessey20_df_reads.csv")
                #df_envis.to_csv(f"{eachDirAddress}111_Bessey20_df_envis.csv")
                #
                #print("len(df_reads.shape[1])", df_reads.shape[1], "<br>")
                #print("df_reads.columns[0]", df_reads.columns[0], "<br>")

                #if df_reads.columns[0] == 'Target':
                #    df_reads.insert(1, 'Samp1', 9999)
                #print("### End pont 10 March. ###<br>")
                #exit()

                list_dfs_cruises_fn.append([cruiseName, fileName_excel, df_sheet_each])


    ### Making sure
    #print("<br># Making sure #<br>")
    #for rec in list_dfs_cruises_fn:
    #    name_cruise = rec[0]
    #    name_excelFile = rec[1]
    #    df_sheet_each = rec[2]
    #    df_reads = df_sheet_each["reads"]
    #    df_envis = df_sheet_each["environments"]
    #    print("name_cruise", name_cruise, "<br>")
    #    print("name_excelFile", name_excelFile, "<br>")
    #    print("df_reads", df_reads, "<br>")
    #    print("df_envis.columns", df_envis.columns, "<br>")
    #    df_reads.to_csv(eachDirAddress + f"910_df_reads_{name_cruise}.csv")
    #    df_envis.to_csv(eachDirAddress + f"910_df_envis_{name_cruise}.csv")
    #    print("<br>")
    #print("### Exit point 7 Mar###<br>")
    #exit()
    return list_dfs_cruises_fn


#def retrieave_environments_from_dataFrame(df_environments):
#    list_environments = []
#    ## https://note.nkmk.me/python-pandas-dataframe-for-iteration/
#    for indexTMP, row in df_environments.iterrows():
#        sampleID_fn = indexTMP
#        #print("sampleID_fn", sampleID_fn, "<br>")
#        cruiseName_env = row['Cruise']
#        station = row['Station']
#        latitude = row['Latitude']
#        longitude = row['Longitude']
#        depth = row['Depth']
#        day = row['Day']
#        list_environments.append([str(sampleID_fn), station, latitude, longitude, depth, day])
#    return list_environments


def retrieave_reads_from_dataFrame(df_reads):
    #print("df_reads", df_reads)
    #exit()
    list_reads = []
    names_column = list(df_reads.columns)
    for sampleID in names_column:
        #print("sampleID", sampleID, "<br>")
        if sampleID == "Target":
            break
        list_sortedSpecies_in_eachSampleID = make_list_sortedSpecies_in_eachSampleID(sampleID, df_reads)
        #list_reads.append([str(sampleID), num_allReads, list_sortedSpecies_in_eachSampleID])
        list_reads.append([str(sampleID), list_sortedSpecies_in_eachSampleID])
    return list_reads


#def changeName_Eng_EngJPN_reads(list_dfs_fn):
#    #print("#### START: changeName_Eng_EngJPN_reads ####<br>")
#    print("Need to add binary_or_not.")
#    exit()
#    list_dfs_cruises_fn = []
#    for rec in list_dfs_fn:
#        cruiseName = rec[0]
#        name_excelFile = rec[1]
#        df_sheet_all = rec[2]
#        #print("### START: cruiseName", cruiseName, "<br>")
#        #print("name_excelFile", name_excelFile, "<br>")
#        #reads_sheet_all["reads"].to_csv('reads_df1_reads.csv')
#
#        list_newNames = []
#        #print("df_sheet_all[reads][Target]1", df_sheet_all["reads"]["Target"], "<br>")
#        for rec1 in df_sheet_all["reads"]["Target"]:
#            recTMP = re.sub("_", "-", rec1)
#            #print("recTMP", recTMP, "<br>")
#            scinetificName_Jname = add_scinetificName_Jname(recTMP)
#            #print("scinetificName_Jname", scinetificName_Jname, "<br>")
#            list_newNames.append(scinetificName_Jname)
#        
#        df_sheet_all["reads"]["Target"] = list_newNames
#        #for newName in list_newNames:
#        #    print("newName", newName, "<br>")
#        #print("df_sheet_all[reads][Target]2", df_sheet_all["reads"]["Target"], "<br>")
#        #print("### END: cruiseName", cruiseName, "<br><br>")
#        #exit()
#
#        list_dfs_cruises_fn.append([cruiseName, name_excelFile, df_sheet_all])
#    #print("#### END: changeName_Eng_EngJPN_reads ####<br>")
#    #exit()
#    return list_dfs_cruises_fn


def changeSpeciesName(list_dfs_fn):
    list_dfs_cruises_fn = []
    for rec in list_dfs_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dic_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dic_df["reads"]
        df_envis = dic_df["environments"]
        
        #print("cruiseName", cruiseName, "<br>")
        #print("name_excelFile", name_excelFile, "<br>")

        dic_df2 = OrderedDict()
        df_reads['Target'] = df_reads['Target'].str.replace('_', '-')
        df_reads['Target'] = df_reads['Target'].str.replace(' ', '-')
        dic_df2["reads"] = df_reads
        dic_df2["environments"] = df_envis
        list_dfs_cruises_fn.append([cruiseName, name_excelFile, dic_df2, binary_or_not])
    return list_dfs_cruises_fn


def make_list_sortedSpecies_in_eachSampleID(sampleID, df_reads):
    #print("### make_list_sortedSpecies_in_eachSampleID")
    list_sortedSpecies_in_eachSampleID = []

    #OTUs_ID, names_species, numbers_of_reads, percents_of_reads = sort_calculatePercents_of_reads_for_one_sampleID(sampleID, df_reads)
    OTUs_ID, names_species, numbers_of_reads = sort_reads_for_one_sampleID(sampleID, df_reads)

    for i in range(len(names_species)):

        numbers_of_reads_TMP = numbers_of_reads[i]
        #print("float(numbers_of_reads_TMP)", float(numbers_of_reads_TMP), "<br>")
        #print("int(numbers_of_reads_TMP)", int(numbers_of_reads_TMP), "<br>")
        #print("readNumber_CompareSpeciesList", readNumber_CompareSpeciesList, "<br>")
        #if readNumber_CompareSpeciesList == "logarithm_transformation":
        #    numbers_of_reads_TMP = float(numbers_of_reads_TMP)
        #else:
        #    numbers_of_reads_TMP = int(numbers_of_reads_TMP)
        numbers_of_reads_TMP = int(numbers_of_reads_TMP)
        if numbers_of_reads_TMP == 0:
            #print("numbers_of_reads_TMP", numbers_of_reads_TMP, "<br><br>")
            break
        #print("<br>")

        list_sortedSpecies_in_eachSampleID.append([names_species[i], numbers_of_reads[i], OTUs_ID[i]])

    return list_sortedSpecies_in_eachSampleID


def calculatePercentage(list2D_cruises_excelFiles_fn):
    list2D_cruises_excelFiles_fn_addPercents = []
    for rec in list2D_cruises_excelFiles_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_environments_reads = rec[2]
        #print("cruiseName",cruiseName)
        #print("name_excelFile",name_excelFile)
        dict_environments_reads["reads"] = calculatePercentage_for_oneReadsSheet(dict_environments_reads["reads"])
        
        #print("dict_environments_reads[reads]",dict_environments_reads["reads"])
        list2D_cruises_excelFiles_fn_addPercents.append([cruiseName, name_excelFile, dict_environments_reads])

    return list2D_cruises_excelFiles_fn_addPercents


#def add_scinetificName_Jname(name_species):
#    #print("name_species", name_species, "<br>")
#    Ename_tmp = re.sub("^[A-Z][A-Z]\d+-", "", name_species)
#    #print("Ename_tmp1", Ename_tmp, "<br>")
#    Ename_tmp = re.sub("^[A-Z]\d+-", "", Ename_tmp)
#    #print("Ename_tmp2", Ename_tmp, "<br>")
#    Jname = dic_scname2jpName.get(Ename_tmp, "不明")
#    Jname = Jname.rstrip("\n")
#    #scinetificName_Jname = name_species + "_" + Jname
#    scinetificName_Jname = Ename_tmp + "_" + Jname
#    #print("scinetificName_Jname", scinetificName_Jname, "<br><br>")
#    return scinetificName_Jname


def exclude_lowReadOTU_readCount_to_ignore(list_dfs_cruises_excelFiles_fn):
    #print("### exclude_lowReadOTU_readCount_to_ignore() ###<br>")
    ## TEST-M22.xlsx を例として開発
    list_dfs_cruises_excelFiles_mod = []
    for rec in list_dfs_cruises_excelFiles_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]

        #binary_or_not = "not-binary"
        #if cruiseName == "User-txt":
        #    binary_or_not = "binary"
        #elif cruiseName == "User-csv":
        #    df_reads_userfile = check_and_read_csv(eachDirAddress + "000_user.csv")
        #    binary_or_not = check_binary_userfile_columns(df_reads_userfile)
        #elif cruiseName == "User-xlsx":
        #    dict_dfs = check_and_read_excel_sheets(eachDirAddress + "000_user.xlsx")
        #    df_reads_userfile = dict_dfs[list(dict_dfs.keys())[0]].reset_index()
        #    binary_or_not = check_binary_userfile_columns(df_reads_userfile)
        #else:
        #    pass

        #print("cruiseName", cruiseName, "<br>")
        #print("binary_or_not", binary_or_not, "<br>")
        dic_df2 = OrderedDict()
        print("ASV_detection_criteria", ASV_detection_criteria, "<br>")
        if binary_or_not == "not-binary" and ASV_detection_criteria != "1":
            print("selected<br>")
            df_reads_new = df_reads.copy()
            df_reads_new.loc[:, ~df_reads_new.columns.isin(['Target'])] = df_reads_new.loc[:, ~df_reads_new.columns.isin(['Target'])].applymap(lambda x: 0 if x < ASV_detection_criteria else x)
            dic_df2["reads"] = df_reads_new
            #print("ASV_detection_criteria done<br>")
        else:
            dic_df2["reads"] = df_reads
            #print("ASV_detection_criteria not<br>")

        dic_df2["environments"] = df_envis
        list_dfs_cruises_excelFiles_mod.append([cruiseName, name_excelFile, dic_df2, binary_or_not])

    return list_dfs_cruises_excelFiles_mod


def extract_list_names_reads_percents_OTUs(list_species_reads):
    #print("extract_list_names_reads_percents_OTUs", extract_list_names_reads_percents_OTUs,"<br>")
    #exit()

    names_species = []
    numbers_of_reads = []
    percents_of_reads = []
    names_OTU = []
    for rec in list_species_reads:
        name_species = rec[0]
        num_reads = rec[1]
        percent_reads = rec[2]
        name_OTU = rec[3]
        names_species.append(name_species)
        numbers_of_reads.append(num_reads)
        percents_of_reads.append(percent_reads)
        names_OTU.append(name_OTU)
    names_species = change_underscore2datash(names_species)
    if names_species:
        names_species = underscoreAdd(names_species)

    return names_species, numbers_of_reads, percents_of_reads, names_OTU


def make_latLongFile_sites_including_pulldownedSpecies_gmt_pd(outFileName, eachDirAddress, list_dfs_cruises):
    print("### make_latLongFile_sites_including_pulldownedSpecies_gmt_pd() ###")
    #print("outFileName", outFileName, "<br>")   # 150_lat_lon_red_selected.txt
    
    list_speciesName_pulldown = get_session_param('list_speciesName_pulldown')

    list_env_specified = []
    for rec in list_dfs_cruises:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dic_sheet = rec[2]
        df_reads = dic_sheet["reads"]
        df_environments = dic_sheet["environments"]
        #fileNameE = eachDirAddress + "035_reads.csv"
        #df_reads.to_csv(fileNameE)
        #fileNameR = eachDirAddress + "035_environments.csv"
        #df_environments.to_csv(fileNameR)
        
        list_sampleID_hit = []
        for name_column in df_reads.columns:
            if name_column == "Target":
                break
            sampleID = name_column

            #### for loop version
            #for species in list_speciesName_pulldown:
            #    #mask = (df_reads["Target"] == species) & (df_reads[name_column] > 0)
            #    # 以下、1と2の条件を、& 演算子を使ってを組み合わせることで、両方の条件を同時に満たす行を選択するマスク（フィルタ）を作成します。
            #    # print("mask", mask, "<br>")
            #    # mask 0 False 1 False 2 True dtype: bool
            #    # mask 0 False 1 False 2 True dtype: bool
            #    # .....
            #    # 2つの条件
            #    # 1. df_reads["Target"] == speciesName_pulldown:
            #    # これは、df_reads データフレームの "Target" 列の値が speciesName_pulldown 変数の値と等しいかどうかをチェックします。
            #    # 結果は、True または False のブール値のシリーズ（列）になります。
            #    # 2. df_reads[name_column] > 0:
            #    # これは、df_reads データフレームの name_column 列の値が0より大きいかどうかをチェックします。
            #    # 結果は、True または False のブール値のシリーズ（列）になります。
            #    
            #    #species = "^" + species + "$"
            #    mask = df_reads["Target"].apply(lambda x: bool(re.search(species, x))) & (df_reads[name_column] > 0)
            #    # re.search はシリーズ全体ではなく、個々の文字列に対して使用する必要があります。
            #    # apply メソッドを使って、シリーズの各要素に対して正規表現検索を適用することができます
            #    # df_reads["Target"] の各要素に対して re.search を適用し、その結果をブール値として返します。
            #    if mask.any():
            #        print("species", species, "<br>")
            #        # mask で True になる行のインデックスを取得
            #        true_indices = df_reads.index[mask]
            #        # そのインデックスに対応する Target 列要素を取得して print
            #        for idx in true_indices:
            #            print("idx:", df_reads.at[idx, "Target"], "<br>")
            #        # そのインデックスに対応する列名を取得
            #        true_columns = df_reads.columns[df_reads.loc[true_indices].any()]
            #        print("true_columns", true_columns, "<br>")
            #        list_sampleID_hit.append(name_column)
            #    #else:
            #    #    print("no mask<br><br>")

            ### apply version
            #mask = df_reads["Target"].apply(lambda x: any(re.search(species, x) for species in list_speciesName_pulldown)) & (df_reads[name_column] > 0)
            mask = df_reads["Target"].apply(lambda x: any(re.search(species, x) for species in list_speciesName_pulldown) if isinstance(x, str) else False) & (df_reads[name_column] > 0)
            if mask.any():
                list_sampleID_hit.append(name_column)
        #print("list_sampleID_hit", list_sampleID_hit, "<br>")
        #exit()
        
        df_filtered_environments = df_environments[df_environments.index.isin(list_sampleID_hit)]
        list_env_specified.extend(df_filtered_environments[['Station', 'Latitude', 'Longitude']].values.tolist())

    with open(eachDirAddress + outFileName, "w") as fs:
        for rec in list_env_specified:
            station, latitude, longitude = rec
            if latitude == "NONE":
                continue
            fs.write(f"{longitude}\t{latitude}\t{station}\n")


def underscoreAdd(names):
    longestName = max(names, key = len)
    longestNameLen = len(longestName)
    newNames = []
    for name in names:
        nameWhiteSpace = name + "___" + "_" * (longestNameLen - len(name) + 2)
        newNames.append(nameWhiteSpace)
    return newNames


def printout_allSpecies_pd(list_dfs_cruises):
    #print("### printout_allSpecies_pd() ###<br>")
    #print("list_cruiseNames", list_cruiseNames, "<br>")
    dic_speciesNames = {}
    for rec in list_dfs_cruises:
        #print("rec", rec, "<br>")
        #for r in rec:
        #    print("r", r, "<br>")
        #    print("<br>")
        cruiseName = rec[0]
        excelFileName = rec[1]
        #exit()
        dic_sheets = rec[2]
        df_reads = dic_sheets["reads"]
        #df_environments = dic_sheets["environments"]
        list_species = df_reads["Target"].tolist()
        
        #print("cruiseName", cruiseName, "<br>")
        #print("excelFileName", excelFileName, "<br>")
        #print("df_reads", df_reads, "<br>")
        #print('df_reads["Target"]', df_reads["Target"], "<br>")
        #fileNameR = eachDirAddress + "030_sheet_reads.csv"
        #df_reads["Target"].to_csv(fileNameR)
        #print("Saved:", fileNameR, "<br>")
        #print("eachDirAddress:", eachDirAddress, "<br>")
        for species in list_species:
            dic_speciesNames[species] = cruiseName
    #exit()    

    list_speciesNames = []
    for species, cruiseName in dic_speciesNames.items():
        #print("11", species, cruiseName, "<br>")
        list_speciesNames.append([species, cruiseName])
    #exit()

    list_speciesNames_sorted_fn = sorted(list_speciesNames, key=lambda x:(x[0]))
    for rec in list_speciesNames_sorted_fn:
        scientificName = rec[0]
        cruiseName_TMP = rec[1]
        #Jname = dic_scname2jpName.get(scientificName, "不明").rstrip("\n")
        name_hit_detected = dic_scname2commonName.get(scientificName, "NA").rstrip("\n")
        print(f'&lt;option value="{scientificName}"&gt;{scientificName}_{name_hit_detected}"&lt;/option&gt;<br>')
    
    return list_speciesNames_sorted_fn

#def check_presenceAbsence_list_speciesNames_SpeciesSearch(list_speciesNames_sorted_fn):
#    #print("### check_presenceAbsence_list_speciesNames_SpeciesSearch() ###<br>")
#
#    flag = 0
#    for rec in list_speciesNames_sorted_fn:
#        species_db = rec[0]
#        #print("species_db1", species_db, "<br>")
#        species_db = re.sub("_.*", "", species_db)
#        #print("species_db2", species_db, "<br>")
#        #print("speciesName_pulldown", speciesName_pulldown, "<br>")
#        if str(speciesName_pulldown) == str(species_db):
#            flag = 1
#    if flag < 1:
#        list_cruiseNames_str = ",".join(list_cruiseNames)
#        #print("searchType", searchType, "<br>")
#        print(speciesName_pulldown, ", was not found in selected cruises, ", list_cruiseNames_str, "<br>")
#        #exit()

def is_number(value):
    # 正規表現で数値かどうかを確認
    if re.match(r'^-?\d+(\.\d+)?$', value):
        return True
    return False

def make_all_latLongfile_for_gmt(outFileName):
    fs = open(eachDirAddress + outFileName, "w") 
    for rec in list_reads_environments:
        #print("rec[4]", rec[4], "<br>")
        sampleID = rec[0]
        station = rec[4]
        latitude = rec[5]
        longitude = rec[6]
        if latitude == "NONE":
            pass
        elif isinstance(latitude, float):
            latitude = round(latitude, 4)
            longitude = round(longitude, 4)
        #fs.write(str(sampleID) + "\t" + str(latitude) + "\t" + str(longitude) + "\n")
        fs.write(str(longitude) + "\t" + str(latitude) + "\t" + str(station) + "\n")
    fs.close()


def is_same_station_name(list_dfs_cruises_fn):
    #print("### is_same_station_name() ###<br>")

    station_sets = []
    for rec in list_dfs_cruises_fn:
        cruiseName_TMP = rec[0]
        name_excelFile_TMP = rec[1]
        dict_df = rec[2]
        df_environments = dict_df["environments"]
        station_sets.append(set(df_environments['Station']))

    # 全てのファイル間で重複をチェック
    duplicates = set()
    for i in range(len(station_sets)):
        for j in range(i + 1, len(station_sets)):
            duplicates.update(station_sets[i].intersection(station_sets[j]))

    if duplicates:
        #print("duplicates", duplicates, "<br>")
        return duplicates
    else:
        #print("no duplicates<br>")
        return None



def make_all_latLongfile_for_gmt_pd(outFileName, eachDirAddress, list_dfs_cruises):
    #print("### make_all_latLongfile_for_gmt_pd() ###<br>")
    #print("outFileName",  outFileName, "<br>")   # 150_lat_lon_white_all.txt

    res_is_same_station_name = is_same_station_name(list_dfs_cruises)
    ### ダブりがあったかどうか判定
    #if res_is_same_station_name:
    #    print(f"Duplicate stations found: {res_is_same_station_name}")
    #else:
    #    print("No duplicate stations found.")
    #exit()

    dic_sta_lat_lon = OrderedDict()
    for rec in list_dfs_cruises:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        df_environments = dict_df["environments"]
        env_dict = df_environments.to_dict('index')
        #print("cruiseName", cruiseName, "<br>")
        for sampleID, row in env_dict.items():
            station = row['Station']
            latitude = row['Latitude']
            longitude = row['Longitude']
            if res_is_same_station_name:
                if cruiseName.startswith("User-"):
                    cruiseName_station = "User_" + station
                else:
                    cruiseName_station = cruiseName + "_" + station
                dic_sta_lat_lon[cruiseName_station] = [latitude, longitude]
            else:
                dic_sta_lat_lon[station] = [latitude, longitude]


    fs = open(eachDirAddress + outFileName, "w")
    for station, lat_lon in dic_sta_lat_lon.items():
        latitude = lat_lon[0]
        longitude = lat_lon[1]
        #print("latitude", latitude, "<br>")
        #print("longitude", longitude, "<br>")
        if latitude == "NONE":
            #print("continue<br>")
            continue
        if float(latitude) == 0 and float(longitude) == 0:
            #print("lat and lon are 0", "<br>")
            continue
        if isinstance(latitude, float):
            latitude = round(latitude, 4)
            longitude = round(longitude, 4)
        fs.write(str(longitude) + "\t" + str(latitude) + "\t" + str(station) + "\n")
        #print("longitude, latitude, station:", longitude, latitude, station, "<br>")
    fs.close()
    
    #print("### Exit point 1111 ###<br>")
    #exit()


################
# Calculate the average Longitude considering the wrap-around at 180 degrees
def calculate_average_longitude(df):
    # Convert longitudes to radians
    df['Longitude_rad'] = df['Longitude'].apply(lambda x: x * (np.pi / 180.0))
    
    # Calculate the average of cosines and sines of longitudes
    avg_cos = df['Longitude_rad'].apply(lambda x: np.cos(x)).mean()
    avg_sin = df['Longitude_rad'].apply(lambda x: np.sin(x)).mean()
    
    # Calculate the average longitude in radians
    avg_longitude_rad = np.arctan2(avg_sin, avg_cos)
    
    # Convert the average longitude back to degrees
    avg_longitude_deg = avg_longitude_rad * (180.0 / np.pi)
    
    return avg_longitude_deg
    
# Function to calculate west_longitude and east_longitude
def calculate_west_east_longitude(longitude, value_to_west, value_to_east):
    # Convert longitude and latitude to radians
    longitude_rad = longitude * (np.pi / 180.0)
    
    # Calculate west_longitude and east_longitude in radians
    west_longitude_rad = longitude_rad - value_to_west * (np.pi / 180.0)
    east_longitude_rad = longitude_rad + value_to_east * (np.pi / 180.0)
    
    # Convert back to degrees
    west_longitude_deg = west_longitude_rad * (180.0 / np.pi)
    east_longitude_deg = east_longitude_rad * (180.0 / np.pi)
    
    return west_longitude_deg, east_longitude_deg

# 経度をラジアンに変換し、180度線を考慮して中央値を計算する関数
#def calculate_median_longitude(df):
#    longitudes = df['Longitude'].apply(lambda x: x if x >= 0 else x + 360)
#    median_longitude = np.median(longitudes)
#    median_longitude = median_longitude if median_longitude <= 180 else median_longitude - 360
#    return median_longitude

#### longitude の range を計算する
# Function to calculate the range of longitude considering the wrap-around at 180 degrees
def calculate_range_longitude(df):
    longitudes = df['Longitude'].apply(lambda x: x if x >= 0 else x + 360)
    range_longitude = longitudes.max() - longitudes.min()
    return range_longitude
# calculate_range_latitude 関数を定義
def calculate_range_latitude(df):
    latitudes = df['Latitude']
    range_latitude = latitudes.max() - latitudes.min()
    return range_latitude

def calculate_center_dist(df):
    # 経度が180度線を跨いでいる場合の中心を計算
    series_longitudes = df['Longitude'].apply(lambda x: x if x >= 0 else x + 360)
    center_longitude = (series_longitudes.max() + series_longitudes.min()) / 2
    if center_longitude > 180:
        center_longitude -= 360
    return center_longitude


def plot_results_by_gmt(list_dfs_cruises, eachDirAddress):
    print("### plot_results_by_gmt() ###")
    
    sitename_map = get_session_param('sitename_map')

    #https://fish-evol.org/GMT_ji.html
    make_all_latLongfile_for_gmt_pd("150_lat_lon_white_all.txt", eachDirAddress, list_dfs_cruises)
    make_latLongFile_sites_including_pulldownedSpecies_gmt_pd("150_lat_lon_red_selected.txt", eachDirAddress, list_dfs_cruises)

    df = pd.read_csv(eachDirAddress + '150_lat_lon_white_all.txt', delimiter='\t', header=None, names=['Longitude', 'Latitude', 'Station'])
    if df.empty:
        return
    
    # Latitude 列から数値以外の値を除外する
    df = df[pd.to_numeric(df['Latitude'], errors='coerce').notnull()]
    
    # Latitude 列あるいは Longitude 列が数値以外の行を除外する
    df['Latitude'] = pd.to_numeric(df['Latitude'])
    df['Longitude'] = pd.to_numeric(df['Longitude'])
    
    # Latitude 列と Longitude 列を数値に変換する
    df['Latitude'] = pd.to_numeric(df['Latitude'])
    df['Longitude'] = pd.to_numeric(df['Longitude'])
    
    # 値が 0 の行を除外する
    df = df[(df['Latitude'] != 0) & (df['Longitude'] != 0)]
    

    ################################################
    # サンプリング分布の中央値 (最大値と最小値の平均) を求める
    # 経度の中央値を計算
    #median_longitude = calculate_median_longitude(df)
    
    # Calculate the ranges in degrees
    range_longitude_deg = calculate_range_longitude(df)
    range_latitude_deg = calculate_range_latitude(df)
    #print("range_longitude_deg", range_longitude_deg, "<br>")
    #print("range_latitude_deg", range_latitude_deg, "<br>")
    
    ################################################
    # 中心となる station の選択
    
    ## 1. ある採水ポイントを selected にする場合
    # Calculate the average Longitude
    #mean_trig_longitude = calculate_average_longitude(df)
    #
    ## Find the Station with the closest Latitude to the average Longitude
    #selected_station = df.iloc[(df['Longitude'] - mean_trig_longitude).abs().argmin()]['Station']
    ##print("selected_station", selected_station)
    #
    #selected_longitude = df[df['Station'] == selected_station]['Longitude'].values[0]
    #selected_latitude = df[df['Station'] == selected_station]['Latitude'].values[0]
    #

    ## 2. 分布の中央を selected にする場合
    center_latitude = (df['Latitude'].max() + df['Latitude'].min()) / 2
    center_longitude = calculate_center_dist(df)
    selected_latitude = center_latitude
    selected_longitude = center_longitude
    
    #print("selected_latitude", selected_latitude, "<br>")
    #print("selected_longitude", selected_longitude, "<br>")
    
    ################################################
    if (120 <= range_longitude_deg) or (90 <= range_latitude_deg):
        map_type = "World-type"
    elif (50 <= range_longitude_deg and range_longitude_deg < 120) or (34 <= range_latitude_deg and range_latitude_deg < 90):
        map_type  = "Large-type"
    elif (16 <= range_longitude_deg and range_longitude_deg < 50) or (16 <= range_latitude_deg and range_latitude_deg < 34):
        map_type  = "Mediam-type"
    elif (4 <= range_longitude_deg and range_longitude_deg < 16) or (7 <= range_latitude_deg and range_latitude_deg < 16):
        map_type  = "Small-type"
    elif (2 <= range_longitude_deg and range_longitude_deg < 4) or (3 <= range_latitude_deg and range_latitude_deg < 7):
        map_type  = "Region-type-L"
    elif (0.9 <= range_longitude_deg and range_longitude_deg < 2) or (0.8 <= range_latitude_deg and range_latitude_deg < 3):
        map_type  = "Region-type-S2"
    else:
        map_type  = "Region-type-S1"

    #print("map_type", map_type, "<br>")
    #########################
    #map_type = "World-type"
    #########################

    if map_type == "World-type":
        map_type_A = "World-type"
        psbasemap_B = "a20f10g10"
        west_tip = -90
        east_tip = 270
        south_tip = -78
        north_tip = 78 #84

    elif map_type == "Large-type":
        psbasemap_B = "a10f10g10"
        #west_tip = selected_longitude - 90
        #east_tip = selected_longitude + 90
        # Calculate west_longitude and east_longitude for St10
        value_to_west = 90
        value_to_east = 90
        west_tip, east_tip = calculate_west_east_longitude(selected_longitude, value_to_west, value_to_east)
    
        if 70 < selected_latitude:
            map_type_A = "Large-type_over70"
            #print("## 1 ##")
            north_tip = selected_latitude + 5
            south_tip = selected_latitude - 45
        elif 58 < selected_latitude and selected_latitude <= 70:
            map_type_A = "Large-type_58_70"
            #print("## 1 ##")
            north_tip = selected_latitude + 20
            south_tip = selected_latitude - 35
        elif 20 < selected_latitude and selected_latitude <= 58:
            map_type_A = "Large-type_20_58"
            north_tip = selected_latitude + 30
            south_tip = selected_latitude - 30
    
        elif -20 < selected_latitude and selected_latitude <= 20:
            map_type_A = "Large-type_-20_20"
            north_tip = selected_latitude + 45
            south_tip = selected_latitude - 45
    
        elif -58 < selected_latitude and selected_latitude <= -20:
            map_type_A = "Large-type_-58_-20"
            north_tip = selected_latitude + 25
            south_tip = selected_latitude - 25
    
        elif -70 < selected_latitude and selected_latitude <= -58:
            map_type_A = "Large-type_under-58"
            north_tip = selected_latitude + 35
            south_tip = selected_latitude - 20
        elif -90 < selected_latitude and selected_latitude <= -70:
            map_type_A = "Large-type_under-70"
            #print("## 1 ##")
            north_tip = selected_latitude + 45
            south_tip = selected_latitude - 5
        else:
            print("Error in GMT mapping: check latitude", selected_latitude)
            #exit()
    
    elif map_type == "Mediam-type":
        psbasemap_B = "a5f6g5"
        map_type_A = "Mediam-typ_A"
        north_tip = selected_latitude + 17
        south_tip = selected_latitude - 17
        west_tip = selected_longitude - 25
        east_tip = selected_longitude + 25
    elif map_type == "Small-type":
        psbasemap_B = "a1f1g1"
        map_type_A = "Small_A"
        north_tip = selected_latitude + 6
        south_tip = selected_latitude - 5
        west_tip = selected_longitude - 8
        east_tip = selected_longitude + 9
    elif map_type == "Region-type-L":
        psbasemap_B = "a1f1g1"
        map_type_A = "Region_L"
        north_tip = selected_latitude + 2.4
        south_tip = selected_latitude - 2.4
        west_tip = selected_longitude - 4
        east_tip = selected_longitude + 4
    elif map_type == "Region-type-S2":
        psbasemap_B = "a1f1g1"
        map_type_A = "Region_S2"
        north_tip = selected_latitude + 1.5
        south_tip = selected_latitude - 1.5
        west_tip = selected_longitude - 3
        east_tip = selected_longitude + 3
    else:
        psbasemap_B = "a0.2f0.2g0.2"
        map_type_A = "Region_S"
        north_tip = selected_latitude + 0.7
        south_tip = selected_latitude - 0.7
        west_tip = selected_longitude - 1.2
        east_tip = selected_longitude + 1.2
    #print("############## map_type_A #############")
    #print("map_type_A", map_type_A, "<br>")
    #print("north_tip", north_tip, "<br>")
    #print("south_tip", south_tip, "<br>")
    #print("west_tip", west_tip, "<br>")
    #print("east_tip", east_tip, "<br>")
    #print("#######################################")
    
    R_grdimage_region = str(west_tip) + "/" + str(east_tip) + "/" + str(south_tip) + "/" + str(north_tip)  # "110/168/-56/-22"
    
    #R_grdimage_region = "124/140/25/36" #"125/139/26/35"
    #R_grdimage_region = "125/139/26/35"
    #print("R_grdimage_region", R_grdimage_region)
    #exit()
    
    ############################
    
    if map_type == "World-type" or map_type == "Large-type":
        '''
        # Create the map and save it as map.ps
        line_pscoast = f"gmt pscoast -Jm1:200000000 -R{R_grdimage_region} -Ggray -Ba30g30 -K > {eachDirAddress}150_map.ps"
        subprocess.call(line_pscoast, shell=True)
        
        line_psxy_w = f"gmt psxy {eachDirAddress}150_lat_lon_white_all.txt -J -R -Sc0.3c -Gwhite -W1p,black -O -K >> {eachDirAddress}150_map.ps"
        subprocess.call(line_psxy_w, shell=True)

        if sitename_map == "shown":
            line_psxy_r = f"gmt psxy {eachDirAddress}150_lat_lon_red_selected.txt -J -R -Sc0.3c -Gred -W1p,black -O -K >> {eachDirAddress}150_map.ps"
            subprocess.call(line_psxy_r, shell=True)

            line_pstext = f"gmt pstext {eachDirAddress}150_lat_lon_white_all.txt -J -R -F+f10p,Helvetica,black+jTL -D0.2c/0.2c -O >> {eachDirAddress}150_map.ps"
            subprocess.call(line_pstext, shell=True)
        else:
            line_psxy_r = f"gmt psxy {eachDirAddress}150_lat_lon_red_selected.txt -J -R -Sc0.3c -Gred -W1p,black -O >> {eachDirAddress}150_map.ps"
            subprocess.call(line_psxy_r, shell=True)
        '''

        #gmt pscoast -R125/139/26/35 -JM24c -Di -Ggray -W0.1,black -K -O -V >> outfiles_py/150_map.ps
        #gmt pscoast -R125/139/-35/-26  -JM24c -Di -Ggray -W0.1,black -K -O -V >> outfiles_py/150_map.ps
        line_pscoast = f"gmt pscoast -R{R_grdimage_region} -JM24c -Di -Ggray -W0.1,black -K >> {eachDirAddress}150_map.ps"
        #print("line_pscoast", line_pscoast, "<br>")
        subprocess.call(line_pscoast, shell=True)
        
        #gmt psbasemap -R125/139/26/35 -JM24c -Ba1f1g1 -BWSne+tKuroshio-region -K -O -V >> outfiles_py/150_map.ps
        #gmt psbasemap -R125/139/-35/-26 -JM24c -Ba1f1g1 -BWSne+tKuroshio-region -K -O -V >> outfiles_py/150_map.ps
        #line_psbasemap = f"gmt psbasemap -R{R_grdimage_region} -JM24c -B{psbasemap_B} -BWSne+t{map_type} -K -O -V >> {eachDirAddress}150_map.ps"
        line_psbasemap = f"gmt psbasemap -R{R_grdimage_region} -JM24c -B{psbasemap_B} -BWSne+t -K -O -V >> {eachDirAddress}150_map.ps"
        #print("line_psbasemap", line_psbasemap, "<br>")
        subprocess.call(line_psbasemap, shell=True)
        #exit()
        
        #psxy 1
        #gmt psxy 150_cruseAll_lat_lon.txt -R -JM -Sc0.40 -W1 -Gwhite -K -O -V >> outfiles_py/150_map.ps
        line_psxy = f"gmt psxy {eachDirAddress}150_lat_lon_white_all.txt -R -JM -Sc0.30 -W1 -Gwhite -K -O -V >> {eachDirAddress}150_map.ps"
        #print("line_psxy", line_psxy, "<br>")
        subprocess.call(line_psxy, shell=True)
        

        if sitename_map == "shown":
            #psxy 2
            #gmt psxy 150_sampleID_lat_lon.txt -R -JM -Sc0.40 -W1 -Gred -O -V >> outfiles_py/150_map.ps
            line_psxy = f"gmt psxy {eachDirAddress}150_lat_lon_red_selected.txt -R -JM -Sc0.30 -W1 -Gred -K -O -V >> {eachDirAddress}150_map.ps"
            #print("line_psxy", line_psxy, "<br>")
            subprocess.call(line_psxy, shell=True)
    
            #gmt pstext 150_cruseAll_lat_lon.txt -R125/139/26/35 -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -K -O -V >> outfiles_py/150_map.ps
            #gmt pstext 150_cruseAll_lat_lon.txt -R125/139/-35/-26 -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -K -O -V >> outfiles_py/150_map.ps
            #line_pstext = f"gmt pstext {eachDirAddress}150_lat_lon_white_all.txt -R{R_grdimage_region} -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -K -O -V >> {eachDirAddress}150_map.ps"
            ##                                                                                                                          black+jBL+Gwhite
            # テキストの位置。http://kdo.la.coocan.jp/gmt13_pstext.html
            line_pstext = f"gmt pstext {eachDirAddress}150_lat_lon_white_all.txt -R{R_grdimage_region} -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -Gwhite -D0.3/-0.15 -O -V >> {eachDirAddress}150_map.ps"
            #print("line_pstext", line_pstext, "<br>")
            subprocess.call(line_pstext, shell=True)
        else:
            #psxy 2
            #gmt psxy 150_sampleID_lat_lon.txt -R -JM -Sc0.40 -W1 -Gred -O -V >> outfiles_py/150_map.ps
            line_psxy = f"gmt psxy {eachDirAddress}150_lat_lon_red_selected.txt -R -JM -Sc0.30 -W1 -Gred -O -V >> {eachDirAddress}150_map.ps"
            #print("line_psxy", line_psxy, "<br>")
            subprocess.call(line_psxy, shell=True)
        
    else:
        #gmt makecpt -Chaxby -T-6000/0/10 -Z > outfiles_py/050_haxby_area.cpt
        line_makecpt = f"gmt makecpt -Chaxby -T-6000/0/10 -Z > {eachDirAddress}050_haxby_area.cpt"
        #print("line_makecpt", line_makecpt, "<br>")
        subprocess.call(line_makecpt, shell=True)
        #exit()
        
        #gmt grdimage ~/ETOPO1_Ice_g_gmt4.grd -R125/139/26/35 -JM24c  -Coutfiles/050_haxby_area.cpt -X1c -Y1c -K >> outfiles_py/150_map.ps
        #gmt grdimage ~/ETOPO1_Ice_g_gmt4.grd -R125/139/-35/-26 -JM24c  -Coutfiles/050_haxby_area.cpt -X1c -Y1c -K >> outfiles_py/150_map.ps
        line_grdimage = f"gmt grdimage {file_grd} -R{R_grdimage_region} -JM24c  -C{eachDirAddress}050_haxby_area.cpt -X1c -Y1c -K >> {eachDirAddress}150_map.ps"
        #print("line_grdimage", line_grdimage, "<br>")
        subprocess.call(line_grdimage, shell=True)
        
        #gmt grdcontour ~/ETOPO1_Ice_g_gmt4.grd -R125/139/26/35 -JM24c -C500 -A500 -L-6000/-0 -W0.1 -K -O -V >> outfiles_py/150_map.ps
        #gmt grdcontour ~/ETOPO1_Ice_g_gmt4.grd -R125/139/-35/-26 -JM24c -C500 -A500 -L-6000/-0 -W0.1 -K -O -V >> outfiles_py/150_map.ps
        line_grdcontour = f"gmt grdcontour {file_grd} -R{R_grdimage_region} -JM24c -C500 -A500 -L-6000/-0 -W0.1 -K -O -V >> {eachDirAddress}150_map.ps"
        #print("line_grdcontour", line_grdcontour, "<br>")
        subprocess.call(line_grdcontour, shell=True)
        #exit()
        
        #gmt pscoast -R125/139/26/35 -JM24c -Di -Ggray -W0.1,black -K -O -V >> outfiles_py/150_map.ps
        #gmt pscoast -R125/139/-35/-26  -JM24c -Di -Ggray -W0.1,black -K -O -V >> outfiles_py/150_map.ps
        line_pscoast = f"gmt pscoast -R{R_grdimage_region} -JM24c -Di -Ggray -W0.1,black -K -O -V >> {eachDirAddress}150_map.ps"
        #print("line_pscoast", line_pscoast, "<br>")
        subprocess.call(line_pscoast, shell=True)
        
        #gmt psscale -D24.5/5/10/0.5 -Coutfiles/050_haxby_area.cpt -Bf1000a2000 -K -O -V >> outfiles_py/150_map.ps
        line_psscale = f"gmt psscale -D24.5/5/10/0.5 -C{eachDirAddress}050_haxby_area.cpt -Bf1000a2000 -K -O -V >> {eachDirAddress}150_map.ps"
        #print("line_psscale", line_psscale, "<br>")
        subprocess.call(line_psscale, shell=True)
        
        #gmt psbasemap -R125/139/26/35 -JM24c -Ba1f1g1 -BWSne+tKuroshio-region -K -O -V >> outfiles_py/150_map.ps
        #gmt psbasemap -R125/139/-35/-26 -JM24c -Ba1f1g1 -BWSne+tKuroshio-region -K -O -V >> outfiles_py/150_map.ps
        #line_psbasemap = f"gmt psbasemap -R{R_grdimage_region} -JM24c -B{psbasemap_B} -BWSne+t{map_type} -K -O -V >> {eachDirAddress}150_map.ps"
        line_psbasemap = f"gmt psbasemap -R{R_grdimage_region} -JM24c -B{psbasemap_B} -BWSne+t -K -O -V >> {eachDirAddress}150_map.ps"
        
        #print("line_psbasemap", line_psbasemap, "<br>")
        subprocess.call(line_psbasemap, shell=True)
        #exit()
        
        #psxy 1
        #gmt psxy 150_cruseAll_lat_lon.txt -R -JM -Sc0.40 -W1 -Gwhite -K -O -V >> outfiles_py/150_map.ps
        line_psxy = f"gmt psxy {eachDirAddress}150_lat_lon_white_all.txt -R -JM -Sc0.40 -W1 -Gwhite -K -O -V >> {eachDirAddress}150_map.ps"
        #print("line_psxy", line_psxy, "<br>")
        subprocess.call(line_psxy, shell=True)
        

        if sitename_map == "shown":
            #psxy 2
            #gmt psxy 150_sampleID_lat_lon.txt -R -JM -Sc0.40 -W1 -Gred -O -V >> outfiles_py/150_map.ps
            line_psxy = f"gmt psxy {eachDirAddress}150_lat_lon_red_selected.txt -R -JM -Sc0.40 -W1 -Gred -K -O -V >> {eachDirAddress}150_map.ps"
            #print("line_psxy", line_psxy, "<br>")
            subprocess.call(line_psxy, shell=True)
    
            #gmt pstext 150_cruseAll_lat_lon.txt -R125/139/26/35 -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -K -O -V >> outfiles_py/150_map.ps
            #gmt pstext 150_cruseAll_lat_lon.txt -R125/139/-35/-26 -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -K -O -V >> outfiles_py/150_map.ps
            #line_pstext = f"gmt pstext {eachDirAddress}150_lat_lon_white_all.txt -R{R_grdimage_region} -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -K -O -V >> {eachDirAddress}150_map.ps"
            ##                                                                                                                          black+jBL+Gwhite
            # テキストの位置。http://kdo.la.coocan.jp/gmt13_pstext.html
            line_pstext = f"gmt pstext {eachDirAddress}150_lat_lon_white_all.txt -R{R_grdimage_region} -JM24c -F+f12p,Helvetica,-=0.5p,black+jBL -Gwhite -D0.3/-0.15 -O -V >> {eachDirAddress}150_map.ps"
            #print("line_pstext", line_pstext, "<br>")
            subprocess.call(line_pstext, shell=True)
        else:
            #psxy 2
            #gmt psxy 150_sampleID_lat_lon.txt -R -JM -Sc0.40 -W1 -Gred -O -V >> outfiles_py/150_map.ps
            line_psxy = f"gmt psxy {eachDirAddress}150_lat_lon_red_selected.txt -R -JM -Sc0.40 -W1 -Gred -O -V >> {eachDirAddress}150_map.ps"
            #print("line_psxy", line_psxy, "<br>")
            subprocess.call(line_psxy, shell=True)

    #psconvert1
    #gmt psconvert outfiles_py/150_map.ps -P -Tg -E200 -V
    line_psconvert = f"gmt psconvert {eachDirAddress}150_map.ps -P -Tg -E200 -V"
    #print("line_psconvert", line_psconvert, "<br>")
    subprocess.call(line_psconvert, shell=True)
    
    #psconvert2
    #gmt psconvert outfiles_py/150_map.ps -P -Tf -E200
    line_psconvert = f"gmt psconvert {eachDirAddress}150_map.ps -P -Tf -E200"
    #print("line_psconvert", line_psconvert, "<br>")
    subprocess.call(line_psconvert, shell=True)
    
    #print("map_type_A", map_type_A)

    #elapsed_time_GMT = round((time.time() - startTime),1)
    #print("GMT が終わるまでにかかった時間: {0}".format(elapsed_time_GMT) + " 秒.<br>")


def makeCount():
    import fcntl
    
    dat = "./" + dir_scripts_oeDNAmap + "count.dat"
    
    fh = open(dat, "r+")
    fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
    
    #countA = fh.read()
    list_countA = list(fh)
    countA = list_countA[-1]
    countA = re.sub(":.*", "", countA)
    #print("countA", countA, "<br>")
    #exit()
    countA = int(countA)
    #print("countA", countA, "<br>")
    #exit()
    
    countB = countA + 1
    now = datetime.date.today()

    fh.seek(0)
    for lineA in list_countA:
        fh.write(str(lineA))
    fh.write(str(countB) + ": " + str(now) + "\n") 
    fcntl.flock(fh.fileno(), fcntl.LOCK_UN)

    fh.close()
    #print("countB", countB, "<br>")
    #exit()
    return str(countB)

#def delete_dirs():
#    now = datetime.date.today()
#    for dir in os.listdir(workDirectory):
#        if re.search("^\d", dir):
#            mtime = datetime.date.fromtimestamp(int(os.path.getmtime(workDirectory + dir)))
#            base, ext = os.path.splitext(dir)
#            if (now - mtime).days >= 3:
#                rm_command = "rm -r " + workDirectory + dir
#                subprocess.call(rm_command, shell=True)


#def make_list_readSumList_for_eachSpecies():
#    print("### make_list_readSumList_for_eachSpecies() ###<br>")
#
#    recs_species_amountList_fn = []
#    for rec in list_reads_environments:
#        #print("rec", rec, "<br>")
#        #exit()
#        sampleID = rec[0]
#        curiseName = rec[1]
#        num_allReads = rec[2]
#        list_species_reads = rec[3]
#        station = rec[4]
#        latitude = rec[5]
#        longitude = rec[6]
#        depth = rec[7]
#        day = rec[8]
#        #print("sampleID", sampleID, "<br>")
#        #print("list_species_reads", list_species_reads, "<br>")
#
#        list_species_percentReads_eachSample = []
#        for speciesname_keyword_tmp in list_speciesNames_sorted:
#            speciesname_keyword = speciesname_keyword_tmp[0]
#            speciesname_keyword = re.sub("_.*$", "", speciesname_keyword)
#            #print("speciesname_keyword", speciesname_keyword, "<br>")
#            #exit()
#
#            hits = []
#            for rec2 in list_species_reads:
#                #exit()
#                name_species_detected = rec2[0]
#                num_reads = rec2[1]
#                name_OTU = rec2[2]
#                #print("name_species_detected", name_species_detected, "<br>")
#                #print("name_species_detected", name_species_detected)
#                #exit()
#                if re.search(speciesname_keyword + "_", name_species_detected):
#                    hits.append([name_species_detected, num_reads, name_OTU])
#            
#            if hits:
#                #print("hits", hits, "<br>")
#                #exit()
#                sum_num_reads = 0
#                for rec in hits:
#                    #name_species_detected = rec[0]
#                    num_reads = rec[1]
#                    #name_OTU = rec[2]
#                    sum_num_reads += num_reads
#                #exit()
#                percent_reads_TMP = int(sum_num_reads)/int(num_allReads) * 100
#                percent_reads = round(percent_reads_TMP, 2)
#                list_species_percentReads_eachSample.append([speciesname_keyword, percent_reads, sum_num_reads])
#            else:
#                list_species_percentReads_eachSample.append([speciesname_keyword, 0, 0])
#            #print("<br>")
#
#        recs_species_amountList_fn.append([sampleID, curiseName, num_allReads, list_species_percentReads_eachSample, station, latitude, longitude, depth, day])
#        #print("<br>")
#    
#    #print("recs_species_amountList_fn", recs_species_amountList_fn)
#    #exit()
#    return recs_species_amountList_fn


def add_environments_2_sampleID(recs_species_amountList):
    #print("recs_species_amountList", recs_species_amountList)
    #exit()
    recs_enviroments_species_amountList = []
    for rec in recs_species_amountList:
        #print("rec1111", rec)
        #exit()
        sampleID = rec[0]
        cruiseName = rec[1]
        sum_reads = rec[2]
        list_speices_amounts = rec[3]
        station = rec[4]
        latitude = rec[5]
        longitude = rec[6]
        depth = rec[7]
        day = rec[8]

        #cruiseName_env, sampleID_env, station_env, latitude_env, longitude_env, depth_env, day_env = retrieve_environmentalParameters_for_a_sampleID(sampleID)
        #print("cruiseName_env", cruiseName_env,"<br>")
        #print("sampleID_env", sampleID_env,"<br>")
        #print("station_env", station_env,"<br>")
        #print("latitude_env", latitude_env,"<br>")
        #print("longitude_env", longitude_env,"<br>")
        #print("depth_env", depth_env,"<br>")
        #print("day_env", day_env,"<br><br>")
        nameLine = str(sampleID) + "_St:" + str(station) + "_Depth:" + str(depth)
        recs_enviroments_species_amountList.append([nameLine, list_speices_amounts])
        #for rec in list_speices_amounts:
        #    print(rec[0], rec[1],"%", rec[2], "reads<br>")
        #print("<br><br>")
        #exit()
    #exit()
    return recs_enviroments_species_amountList


#def convert_list_2_matrix_4_pheatmap(recs_enviroments_species_amountList_tmp):
#
#    #print("recs_enviroments_species_amountList_tmp[0]", recs_enviroments_species_amountList_tmp[0], "<br><br>")
#
#    ###### Percent: making matrix 4 matrix_4_pheatmap
#    csvList_for_pheatmap_percent = []
#    csvList_for_pheatmap_reads = []
#
#    #### 1st line
#    line_columnName = []
#    line_columnName.append("SampleID")
#    list_speciesName = recs_enviroments_species_amountList_tmp[0][1]
#    for speciesName in list_speciesName:
#        line_columnName.append(speciesName[0])
#    csvList_for_pheatmap_percent.append(line_columnName)
#    csvList_for_pheatmap_reads.append(line_columnName)
#
#    #### 2nd and later lines
#    for rec in recs_enviroments_species_amountList_tmp:
#        #print("rec111", rec)
#        #exit()
#        line_2nd_and_later_percent = []
#        line_2nd_and_later_reads = []
#        sampleID = rec[0]
#        list_species_percent = rec[1]
#        line_2nd_and_later_percent.append(sampleID)
#        line_2nd_and_later_reads.append(sampleID)
#        for rec2 in list_species_percent:
#            name_species = rec2[0]
#            value_percent = rec2[1]
#            value_read = rec2[2]
#            line_2nd_and_later_percent.append(value_percent)
#            line_2nd_and_later_reads.append(value_read)
#        csvList_for_pheatmap_percent.append(line_2nd_and_later_percent)
#        csvList_for_pheatmap_reads.append(line_2nd_and_later_reads)
#    
#    #for line in csvList_for_pheatmap_reads:
#    #    print("line11", line, "<br>")
#    #exit()
#
#    #csvList_for_pheatmap_percent_turned = turn_matrix1(csvList_for_pheatmap_percent)
#    #csvList_for_pheatmap_reads_turned = turn_matrix1(csvList_for_pheatmap_reads)
#
#    #return csvList_for_pheatmap_percent_turned, csvList_for_pheatmap_reads_turned
#    return csvList_for_pheatmap_percent, csvList_for_pheatmap_reads


def turn_matrix1(matrix):
    x = len(matrix)
    y = len(matrix[0])
    turned = []
    for i in range(y):
        tmp = []
        for j in range(x):
            tmp.append(matrix[j][i])
        turned.append(tmp)
    return turned


def pheatmap_R(eachDirAddress, infile4pheatmap, outfile):
    #print("### pheatmap_R() ###<br>")
    #print("dir_scripts_oeDNAmap", dir_scripts_oeDNAmap, "<br>")
    #print("eachDirAddress", eachDirAddress, "<br>")
    #print("infile4pheatmap", infile4pheatmap, "<br>")
    #print("index_distance", index_distance, "<br>")
    #print("outfile", outfile, "<br>")
    
    index_distance = get_session_param('index_distance')
    
    pheatLine = dir_scripts_oeDNAmap + "Rscript " + dir_scripts_oeDNAmap + "pheatmap.R " + eachDirAddress + infile4pheatmap + " " + index_distance + " " + eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + "_log.txt"
    #pheatLine = f"{dir_scripts_oeDNAmap}Rscript {dir_scripts_oeDNAmap}pheatmap.R {eachDirAddress}{infile4pheatmap} {index_distance} {eachDirAddress}{outfile}.pdf > {eachDirAddress}{outfile}_log.txt"
    #print ("pheatLine: ", pheatLine, "<br>")
    #exit()
    subprocess.call(pheatLine, shell=True)

    line_pdftoppm = "pdftoppm -png -scale-to 2048 " +  eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + ".png"
    #print(line_pdftoppm + "<br>")
    subprocess.call(line_pdftoppm, shell=True)


def pheatmap_depth_R(infile4pheatmap, eachDirAddress, outfile):
    #print("### pheatmap_R() ###<br>")
    pheatLine = dir_scripts_oeDNAmap + "Rscript " + dir_scripts_oeDNAmap + "pheatmap.R " + eachDirAddress + infile4pheatmap + " bray " + eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + "_log.txt"
    #print ("pheatLine: ", pheatLine, "<br>")
    #exit()
    subprocess.call(pheatLine, shell=True)

    line_pdftoppm = "pdftoppm -png -scale-to 2048 " +  eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + ".png"
    #print("line_pdftoppm:", line_pdftoppm + "<br>")
    subprocess.call(line_pdftoppm, shell=True)


def hclust_R(infile4pheatmap, eachDirAddress, outfile):

    index_distance = get_session_param('index_distance')

    hclustLine = dir_scripts_oeDNAmap + "Rscript " + dir_scripts_oeDNAmap + "hclust.R " + eachDirAddress + infile4pheatmap + " " + index_distance + " " + eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + "_log.txt"
    #print ("hclustLine: ", hclustLine, "<br>")
    #exit()
    subprocess.call(hclustLine, shell=True)

    line_pdftoppm = "pdftoppm -png -scale-to 2048 " +  eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + ".png"
    #print(line_pdftoppm + "<br>")
    subprocess.call(line_pdftoppm, shell=True)

def nMDS_R(infile4pheatmap, eachDirAddress, outfile):
    #print("### nMDS_R ###<br>")
    #print("infile4pheatmap", infile4pheatmap, "<br>")

    index_distance = get_session_param('index_distance')

    nMDS_line = dir_scripts_oeDNAmap + "Rscript " + dir_scripts_oeDNAmap + "nMDS.R " + eachDirAddress + infile4pheatmap + " " + index_distance + " " + eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + "_log.txt"
    #print ("nMDS_line: ", nMDS_line, "<br>")
    #exit()
    subprocess.call(nMDS_line, shell=True)

    line_pdftoppm = "pdftoppm -png -scale-to 2048 " +  eachDirAddress + outfile + ".pdf > " + eachDirAddress + outfile + ".png"
    #print(line_pdftoppm + "<br>")
    subprocess.call(line_pdftoppm, shell=True)


#def select_specimens_including_pulledownedSpecies():
#    print("### select_specimens_including_pulledownedSpecies() ###<br>")
#    list_speciesList_selected = []
#    if speciesName_pulldown == "NONE":
#        for rec in list_reads_environments:
#            #sampleID = rec[1]
#            #print("sampleID", sampleID, "<br>")
#            list_speciesList_selected.append(rec)
#    else:
#        for rec in list_reads_environments:
#            #print("rec", rec, "<br>")
#            #exit()
#            sampleID_TMP = rec[0]
#            cruiseName_TMP = rec[1]
#            num_allReads = rec[2]
#            list_species = rec[3]
#            hit = 0
#            for species_with_readInfo in list_species:
#                print("speciesName_pulldown", speciesName_pulldown, "<br>")
#                print("species_with_readInfo", species_with_readInfo, "<br>")
#                species_detected = species_with_readInfo[0]
#                print("species_detected", species_detected, "<br>")
#                #print("species_detected", species_detected, "<br>")
#                if re.search(str(speciesName_pulldown), str(species_detected)):
#                    print("found<br>")
#                    hit += 1
#                else:
#                    print("not found<br>")
#                    pass
#                print("<br>")
#            if hit > 0:
#                list_speciesList_selected.append(rec)
#            #print("<br>")
#    
#    return list_speciesList_selected


#def bold_selectedSpecies(list_speciesList_selected):
#    #print("list_speciesList_selected", list_speciesList_selected)
#    #exit()
#    list_speciesList_selected_modified = []
#    for rec in list_speciesList_selected:
#        sampleID = rec[0]
#        cruiseName = rec[1]
#        num_allReads = rec[2]
#        list_species = rec[3]
#        station = rec[4]
#        latitude = rec[5]
#        longitude = rec[6]
#        depth = rec[7]
#        day = rec[8]
#
#        list_species_modified = []
#        for species_with_readFraction in list_species:
#            #if len(list_speciesNames_pulldown) > 1:
#            #    if re.search(str(list_speciesNames_pulldown[i]), str(species_with_readFraction)):
#            #        species_with_readFraction = "<b>" + species_with_readFraction + "</b>"
#            #else:
#            #    if re.search(str(list_speciesNames_pulldown[0]), str(species_with_readFraction)):
#            #        species_with_readFraction = "<b>" + species_with_readFraction + "</b>"
#            if re.search(str(speciesName_pulldown), str(species_with_readFraction)):
#                species_with_readFraction = "<b>" + species_with_readFraction + "</b>"
#            list_species_modified.append(species_with_readFraction)
#        list_speciesList_selected_modified.append([sampleID, cruiseName, num_allReads, list_species_modified, station, latitude, longitude, depth, day])
#
#    return list_speciesList_selected_modified


#def make_list_sequenceName_selected(list_speciesList_selected, i):
#    list_sequenceList_selectedSpecies = []
#    for rec in list_speciesList_selected:
#        sampleID = rec[0]
#        cruiseName = rec[1]
#        num_allReads = rec[2]
#        list_species = rec[3]
#        station = rec[4]
#        latitude = rec[5]
#        longitude = rec[6]
#        depth = rec[7]
#        day = rec[8]
#
#        list_species_selected = []
#        for species_with_readFraction in list_species:
#            if re.search(str(speciesName_pulldown), str(species_with_readFraction)):
#                list_species_selected.append(species_with_readFraction)
#        
#        if list_species_selected:
#            list_sequenceList_selectedSpecies.append([sampleID, cruiseName, num_allReads, list_species_selected, station, latitude, longitude, depth, day])
#
#    return list_sequenceList_selectedSpecies


#def readFasta_dict(InfileNameFN):
#    Infile = open(InfileNameFN, "r")
#    seqDictFN  = OrderedDict()
#    for Line in Infile:
#        Line = Line.rstrip("\n")
#        if Line[0] == ">":
#            Name = Line
#            Name = re.sub(" +$", "", Name)
#            seqDictFN[Name] = ""
#        else:
#            seqDictFN[Name] += Line
#    Infile.close()
#    return seqDictFN


#def makeList_species_numSeq(outFileName):
#    #print("## make_fast_sequenceName_selected starts", i, "<br>")
#    #exit()
#    #print("eachDirAddress", eachDirAddress, "<br>")
#    #exit()
#    dic_species_seqNum = {}
#    for rec in list_reads_environments:
#        sampleID = rec[0]
#        cruiseName = rec[1]
#        num_allReads = rec[2]
#        list_species = rec[3]
#        station = rec[4]
#        latitude = rec[5]
#        longitude = rec[6]
#        depth = rec[7]
#        day = rec[8]
#
#        #print("sampleID", sampleID, "<br>")
#        for species_db in list_species:
#            #print("species_db", species_db, "<br>")
#            species_detected = species_db[0]
#            species_detected = re.sub("_.*", "", species_detected)
#            if species_detected in dic_species_seqNum:
#                dic_species_seqNum[species_detected] += 1
#            else:
#                dic_species_seqNum[species_detected] = 1
#
#    list_species_seqNum = []
#    for spName, num_seq in dic_species_seqNum.items():
#        list_species_seqNum.append([spName,num_seq])
#
#    list_species_seqNum_sorted = sorted(list_species_seqNum, key=lambda x:-(x[1]))
#
#    fs = open(eachDirAddress + outFileName, "w")
#    for rec in list_species_seqNum_sorted:
#        speciesName = rec[0]
#        seq_num = rec[1]
#        species_detected = re.sub("-[^-]+$", "", speciesName)
#        fs.write(species_detected + "," + str(seq_num) + "\n")
#    fs.close()


def changeNameLine_trimalOutName (eachDirAddressFN, infile, outfile):
    recsFN = readFasta_dict(eachDirAddressFN + infile)
    out=open(eachDirAddressFN + "/" +outfile, "w")
    for name,seq in recsFN.items():
        name = re.sub(" .*$", "", name)
        out.write(name + "\n")
        out.write(seq + "\n")
    out.close()


def outGroupSelect(fastaFile):
    #recSeqFN = readPhy_dict(phyFileName)
    recsFN = readFasta_dict(eachDirAddress + fastaFile)

    #outgroupTMP = list(recsFN.keys())[-1]
    outgroupTMP = list(recsFN.keys())[0]
    #print("outgroupTMP", outgroupTMP, "<br>")
    #exit()
    return outgroupTMP[1:]


###  others
def compression(eachDirAddress, dirName_count, list_cruiseNames, input_file_userDB, PDF_file, database_address):
    #print("### compression() ###<br>")

    resDirName = eachDirAddress + "result" + str(dirName_count)
    os.mkdir (resDirName)

    #shutil.copy(eachDirAddress + "300_results.html", resDirName + "/010_results.html")
    lines300 = open(eachDirAddress + "300_results.html")
    out300_150 = open(resDirName + "/010_results.html", "w")
    for line in lines300:
        if not re.search("Download:", line):
            out300_150.write(line)
    out300_150.close()

    if os.path.exists(eachDirAddress + "150_map.png"):    
        #shutil.copy(eachDirAddress + "150_map.ps", resDirName + "/")
        shutil.copy(eachDirAddress + "150_map.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "150_map.pdf", resDirName + "/")

    #shutil.copy(eachDirAddress + "400_fasta.txt", resDirName + "/")
    #if os.path.isfile(eachDirAddress + "515_tree_unrooted.pdf"):
    #    shutil.copy(eachDirAddress + "515_tree_unrooted.pdf", resDirName + "/")
    #    shutil.copy(eachDirAddress + "515_tree_unrooted.png", resDirName + "/")
    #if os.path.isfile(eachDirAddress + "400_species_detectedFrequencies.csv"):
    #    shutil.copy(eachDirAddress + "400_species_detectedFrequencies.csv", resDirName + "/")
    

    #shutil.copy(eachDirAddress + "200_communityData4R_percent.csv", resDirName + "/")
    shutil.copy(eachDirAddress + "200_communityData4R.csv", resDirName + "/")
    shutil.copy(eachDirAddress + "200_communityData4R_station.csv", resDirName + "/")
    if len(list_cruiseNames) <  2:
        shutil.copy(eachDirAddress + "200_communityData4R_depth.csv", resDirName + "/")
    shutil.copy(eachDirAddress + "200_environmentData4R.csv", resDirName + "/")

    shutil.copy(dir_scripts_oeDNAmap + "pheatmap.R", resDirName + "/610_pheatmap.R")
    if os.path.exists(eachDirAddress + "210_pheatmap.png"):
        shutil.copy(eachDirAddress + "210_pheatmap.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "210_pheatmap.pdf", resDirName + "/")
    if os.path.exists(eachDirAddress + "210_pheatmap_station.png"):    
        shutil.copy(eachDirAddress + "210_pheatmap_station.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "210_pheatmap_station.pdf", resDirName + "/")
    if os.path.exists(eachDirAddress + "210_pheatmap_depth.png"):    
        shutil.copy(eachDirAddress + "210_pheatmap_depth.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "210_pheatmap_depth.pdf", resDirName + "/")

    shutil.copy(dir_scripts_oeDNAmap + "nMDS.R", resDirName + "/620_nMDS.R")
    shutil.copy(dir_scripts_oeDNAmap + "permanova.R", resDirName + "/625_permanova.R")
    if os.path.exists(eachDirAddress + "220_nMDS.png"):
        shutil.copy(eachDirAddress + "220_nMDS.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "220_nMDS.pdf", resDirName + "/")
    if os.path.exists(eachDirAddress + "220_nMDS_station.png"):
        shutil.copy(eachDirAddress + "220_nMDS_station.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "220_nMDS_station.pdf", resDirName + "/")

    shutil.copy(dir_scripts_oeDNAmap + "hclust.R", resDirName + "/630_hclust.R")
    if os.path.exists(eachDirAddress + "230_hclust.png"):    
        shutil.copy(eachDirAddress + "230_hclust.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "230_hclust.pdf", resDirName + "/")
    if os.path.exists(eachDirAddress + "230_hclust_station.png"):    
        shutil.copy(eachDirAddress + "230_hclust_station.png", resDirName + "/")
        if PDF_file == "create":
            shutil.copy(eachDirAddress + "230_hclust_station.pdf", resDirName + "/")

    #shutil.copy(dir_scripts_oeDNAmap + "permanova.R", resDirName + "/640_permanova.R")


    files_and_directories = os.listdir(eachDirAddress)
    #print("eachDirAddress", eachDirAddress, "<br>")
    for file in files_and_directories:
        if file.startswith("500_"):
            shutil.copy(eachDirAddress + file, resDirName + "/")

    for cruiseName in list_cruiseNames:
        #print("cruiseName", cruiseName, "<br>")
        if cruiseName.startswith("User-"):
            if os.path.exists(eachDirAddress + "000_user.xlsx"):
                shutil.copy(eachDirAddress + "000_user.xlsx", resDirName + f"/000_{input_file_userDB.filename}")
            elif os.path.exists(eachDirAddress + "000_user.csv"):
                shutil.copy(eachDirAddress + "000_user.csv", resDirName + f"/000_{input_file_userDB.filename}")
            elif os.path.exists(eachDirAddress + "000_user.txt"):
                shutil.copy(eachDirAddress + "000_user.txt", resDirName + f"/000_{input_file_userDB.filename}")
            else:
                print("Error: check 000_user.* file.<br>")
                exit()
        else:
            list_excelFile = dics_cruiseName_excelFiles[cruiseName]
            #print("resDirName", resDirName, "<br>")
            for excelFile in list_excelFile:
                #print("excelFile", excelFile, "<br>")
                shutil.copy(database_address + excelFile, resDirName + "/000_" + excelFile)

    #### Check log 
    #line_mv = "mv " + eachDirAddress + "*.csv " + resDirName + "/"
    #print("line_mv", line_mv, "<br>")
    #subprocess.call(line_mv, shell=True)
    #### 

    zipfiles = glob.glob(resDirName + '/*')
    #fzip = zipfile.ZipFile(resDirName + '_oeDNAmap.zip', 'w', zipfile.ZIP_DEFLATED)
    fzip = zipfile.ZipFile(eachDirAddress + 'result' + str(dirName_count) + '_oeDNAmap.zip', 'w', zipfile.ZIP_DEFLATED)
    #print("#### fzip", fzip)
    for file in zipfiles:
        fzip.write(file, os.path.basename(file))
    fzip.close()




############################################ A0

def change_nameLine(eachDirAddressFN, infile, out_namechanged_uploaded):
    recsFN = readFasta_dict(eachDirAddressFN + infile)
    out = open(eachDirAddressFN + out_namechanged_uploaded, "w")
    count_yourseq = 1
    for name ,seq in recsFN.items():
        name_new = re.sub(r"\(", "", name)
        name_new = re.sub(r"\)", "", name_new)
        #name_new =re.sub("_", "-", name_new)
        name_new =re.sub(" ", "-", name_new)
        name_new =re.sub(",", "-", name_new)
        name_new = re.sub("(>.{70}).*", r"\1", name_new)

        name_new = re.sub("^>", ">YOURSEQ" + str(count_yourseq) + "_", name_new)

        out.write(name_new + "\n")
        seq =re.sub(" ", "-", seq)
        seq =re.sub("-", "", seq)
        out.write(seq + "\n")
        count_yourseq += 1
    out.close()
    

#def read_blastnRes2(infileFN):
#    f = open(infileFN)
#    lines = list(f)
#    f.close()
#
#    list_each_database = get_each_database(lines)
#    list_each_blasthit_raw = clean_each_blasthit(list_each_database)
#    #print("list_each_blasthit_raw", list_each_blasthit_raw)
#    #exit()
#    list_each_blasthit = clean_each_blasthit2(list_each_blasthit_raw)
#
#    return list_each_blasthit

#def get_each_database(lines_fn):
#    dic_each_database_fn = OrderedDict()
#    flag = 0
#    database = ""
#    lines_stock = []
#    nameline = ""
#    flag_nameline = 0
#    for line in lines_fn:
#        line = line.rstrip("\n")
#        if line.startswith("Database:"):
#            if flag == 1:
#                 dic_each_database_fn[database] = lines_stock
#                 database = line
#                 lines_stock = []
#            if flag == 0:
#                database = line
#                flag = 1
#        else:
#            if line.startswith("Query=") or line.startswith(" Score") or line.startswith(" Identities") or line.startswith(" Strand") or line.startswith("Sbjct") or line.startswith("***** No hits found *****"):
#                lines_stock.append(line)
#
#            if flag_nameline == 1:
#                if line.startswith("Length"):
#                    lines_stock.append(nameline)
#                    nameline = ""
#                    lines_stock.append(line)
#                    flag_nameline = 0
#                else:
#                    nameline += line
#            else:
#                if line.startswith(">"):
#                    nameline = line
#                    flag_nameline = 1
#                
#    dic_each_database_fn[database] = lines_stock
#
#    list_each_query_fn = []
#    for database, recs in dic_each_database_fn.items():
#        list_each_query_fn.append([database, recs])
#
#    return list_each_query_fn
    

#def clean_each_blasthit(list_each_query_fn):
#    list_each_blasthit_fn = []
#    query = ""
#    nameline = ""
#    for ele in list_each_query_fn:
#        database = ele[0]
#        lines = ele[1]
#        for line in lines:
#            if not line:
#                continue
#            if line.startswith("Query"):
#                query = line
#                nameline = ""
#            elif line == "***** No hits found *****":
#                list_each_blasthit_fn.append([database, query, ">" + line, ">" + line])
#            elif line.startswith(">"):
#                nameline = line
#                #nameline = re.sub(" .*$", "", nameline)
#                list_each_blasthit_fn.append([database, query, nameline, nameline])
#            else:
#                list_each_blasthit_fn.append([database, query, nameline, line])
#    return list_each_blasthit_fn


#def clean_each_blasthit2(list_each_query_fn):
#    list_each_query2_fn = []
#    flag = 0
#    database_stock = ""
#    query_stock = ""
#    nameline_stock = ""
#    length_stock = ""
#    score_stock = ""
#    identity_stock = ""
#    strand_stock = ""
#    sbjct_stock = []
#    for line in list_each_query_fn:
#        database = line[0]
#        query = line[1]
#        content = line[3]
#        #print(line)
#        #continue
#        #'''
#        if content.startswith(">"):
#            #print(content)
#            if flag == 0:
#                #print("flag == 0", content)
#                #print("content", content)
#                #exit()
#                nameline_stock = content
#                database_stock = database
#                query_stock = query
#                flag = 1
#            else:
#                list_each_query2_fn.append([database_stock, query_stock, nameline_stock, length_stock,score_stock, identity_stock, strand_stock, sbjct_stock])
#                database_stock = database
#                query_stock = query
#                nameline_stock = content
#                length_stock = ""
#                score_stock = ""
#                identity_stock = ""
#                strand_stock = ""
#                sbjct_stock = []
#        elif content.startswith("Length="):
#            length_stock = content
#        elif content.startswith(" Score ="):
#            score_stock = content
#        elif content.startswith(" Identities ="):
#            identity_stock = content
#        elif content.startswith(" Strand="):
#            strand_stock = content
#        elif content.startswith("Sbjct  "):
#            sbjct_1, sbjct_2 = make_sbjct_stock(content)
#            #print(sbjct_1, sbcjt_2)
#            #exit()
#            sbjct_stock.append(sbjct_1)
#            sbjct_stock.append(sbjct_2)
#        #'''
#    #print("database_stock", database_stock)
#    #print("query_stock", query_stock)
#    #print("nameline_stock", nameline_stock)
#    #print("length_stock", length_stock)
#    #print("score_stock", score_stock)
#    #print("identity_stock", identity_stock)
#    #print("strand_stock", strand_stock)
#    #print("sbjct_stock", sbjct_stock)
#    list_each_query2_fn.append([database_stock, query_stock, nameline_stock, length_stock, score_stock, identity_stock, strand_stock, sbjct_stock])
#    
#    return list_each_query2_fn


#def make_sbjct_stock(line_sbjct):
#    #print("line_sbjct", line_sbjct)
#    match = re.search("Sbjct +(\d+) +[^ ]+ +(\d+)$", line_sbjct)
#    former = match.group(1)
#    latter = match.group(2)
#    return former, latter

def merge_ASV_2_Species(list_dfs_cruises_excelFiles_fn):
    #print("### merge_ASV_2_Species() ###<br>")
    list_dfs_cruises_excelFiles_fn_mod = []

    #print("cruiseName_html", cruiseName_html, "<br>")
    for rec in list_dfs_cruises_excelFiles_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]
        #print("cruiseName", cruiseName, "<br>")
        #print("name_excelFile", name_excelFile, "<br>")
        #print("df_reads['Target']", df_reads['Target'], "<br>")

        #print("Merge columns with the same name.<br>")
        df_reads_gp = ""
        if df_reads.duplicated(subset=['Target']).any():
            df_reads_gp = df_reads.groupby('Target').sum().reset_index()
        else:
            df_reads_gp = df_reads
        #print("df_reads_gp['Target']", df_reads_gp['Target'], "<br>")

        dct_dfs = OrderedDict()
        dct_dfs["reads"] = df_reads_gp
        dct_dfs["environments"] = df_envis

        list_dfs_cruises_excelFiles_fn_mod.append([cruiseName, name_excelFile, dct_dfs, binary_or_not])
        
    #exit()
    return list_dfs_cruises_excelFiles_fn_mod


def merge_oneCruseSeveralDFs_to_1df(list_dfs_cruises_excelFiles_fn):
    #print("### merge_oneCruseSeveralDFs_to_1df() ###")
    list_dfs_cruises_excelFiles_fn_mod = []
    
    list_cruiseNames = get_session_param('list_cruiseNames')
    
    for cruiseName_html in list_cruiseNames:
        #print("cruiseName_html", cruiseName_html, "<br>")
        list_df_reads = []
        list_df_envis = []
        list_binary_or_not = []
        for rec in list_dfs_cruises_excelFiles_fn:
            cruiseName_df = rec[0]
            name_excelFile = rec[1]
            dict_df = rec[2]
            binary_or_not = rec[3]
            df_reads = dict_df["reads"]
            df_envis = dict_df["environments"]
            if cruiseName_html == cruiseName_df:
                #print("df_reads.index", df_reads.index,"<br>")
                #df_reads = df_reads.reset_index()
                list_df_reads.append(df_reads)
                #df_reads.to_csv(eachDirAddress + "010_" + cruiseName_df + "_" + name_excelFile + "_reads.csv")
                list_df_envis.append(df_envis)
                #df_envis.to_csv(eachDirAddress + "010_" + cruiseName_df + "_" + name_excelFile + "_envis.csv")
                list_binary_or_not.append(binary_or_not)

        ### read table
        df_reads_merged = reduce(lambda left, right: pd.merge(left, right, on='Target', how='outer'), list_df_reads)

        # 'Target' 列を最後に移動
        cols = df_reads_merged.columns.tolist()
        cols.remove('Target')
        cols.append('Target')
        # 列の順序を再設定
        df_reads_merged = df_reads_merged[cols]
        df_reads_merged = df_reads_merged.fillna(0)

        dct_dfs = OrderedDict()
        dct_dfs["reads"] = df_reads_merged
        #df_reads_merged.to_csv(eachDirAddress + "012_" + cruiseName_html + "_reads.csv")

        ### environment table
        df_envis_concat_TMP = pd.concat(list_df_envis, axis=0)
        #df_envis_concat_TMP.to_csv(eachDirAddress + "012_" + cruiseName_html + "_envis_TMP.csv")
        #print("df_envis_concat_TMP.index", df_envis_concat_TMP.index, "<br>")
        #df_envis_concat = df_envis_concat_TMP.drop_duplicates()
        df_envis_concat = df_envis_concat_TMP[~df_envis_concat_TMP.index.duplicated(keep='first')]
        #print("df_envis_concat.index", df_envis_concat.index, "<br>")
        #exit()
        #df_envis_concat.to_csv(eachDirAddress + "015_" + cruiseName_html + "_envis.csv")
        dct_dfs["environments"] = df_envis_concat
        
        list_dfs_cruises_excelFiles_fn_mod.append([cruiseName_html, "DAMMY", dct_dfs, list_binary_or_not[0]])
    #print("### abort point 3848 ###")
    #abort(400)
    return list_dfs_cruises_excelFiles_fn_mod


def merge_depth_to_station(list_dfs_cruises_excelFiles_fn):
    #print("### merge_depth_to_station ###<br>")
    list_dfs_cruises_stations_fn = []

    for rec in list_dfs_cruises_excelFiles_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]
        
        #### Printout for making sure
        #df_reads.to_csv(eachDirAddress + "200_df_df_reads.csv")
        
        # 'Station'ごとに'SampleID'をリスト化するための辞書を作成
        dict_station_TMP = OrderedDict()
        # 変更前
        #for index, row in df_envis.iterrows():
        #    if row['Station'] not in dict_station_TMP:
        #        dict_station_TMP[row['Station']] = []
        #    dict_station_TMP[row['Station']].append(index)
        # 'Station'ごとに'SampleID'をリスト化するための辞書を作成
        # 変更後
        obj_pd_grouped = df_envis.groupby('Station')
        # obj_pd_grouped は、pandasのDataFrameGroupByオブジェクトです。
        # このオブジェクトは、groupbyメソッドを使用してデータフレームをグループ化した結果を表します。
        for station, df_group in obj_pd_grouped:
            #print(f"Station: {station}<br>")
            #print(f"Group.index: {df_group.index}<br>")
            dict_station_TMP[station] = df_group.index.tolist()
        #exit()
        
        ### Delete SampleID according to the reads sheet columns
        dict_station = OrderedDict()
        for station, list_sampleIDs  in dict_station_TMP.items():
            #print("station", station, "<br>")
            #print("list_sampleIDs", list_sampleIDs, "<br>")
            list_sampleID_selected = []
            for sampleID in list_sampleIDs:
                if sampleID in df_reads.columns.tolist():
                    list_sampleID_selected.append(sampleID)
            dict_station[station] = list_sampleID_selected

        # 新しいデータフレームを作成
        df_reads_new = pd.DataFrame()
        for station, list_sampleIDs  in dict_station.items():
            if len(list_sampleIDs):
                df_reads_new[station] = df_reads[list_sampleIDs].sum(axis=1)
        # Target 列を df_reads_new に加える
        df_reads_new['Target'] = df_reads['Target']

        #### Printout for making sure
        #df_reads_new.to_csv(eachDirAddress + "210_df_reads_station.csv")
        
        ## 格納
        dct_dfs = OrderedDict()
        dct_dfs["reads"] = df_reads_new
        dct_dfs["environments"] = df_envis

        list_dfs_cruises_stations_fn.append([cruiseName, name_excelFile, dct_dfs, binary_or_not])

    return list_dfs_cruises_stations_fn


def merge_station_to_depth(list_dfs_cruises_excelFiles_fn, eachDirAddress):
    #print("### merge_station_to_depth ###<br>")
    list_dfs_cruises_depths_fn = []

    for rec in list_dfs_cruises_excelFiles_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]
        
        #print("cruiseName", cruiseName, "<br>")
        #print("name_excelFile", name_excelFile, "<br>")
        
        #### Printout for making sure
        #df_reads.to_csv(eachDirAddress + "200_df_df_reads.csv")
        
        # 'Depth'ごとに'SampleID'をリスト化するための辞書を作成
        dict_station_TMP = OrderedDict()
        #print("df_envis.columns", df_envis.columns, "<br>")
        #exit()
        obj_pd_grouped = df_envis.groupby('Depth')
        # obj_pd_grouped は、pandasのDataFrameGroupByオブジェクトです。
        # このオブジェクトは、groupbyメソッドを使用してデータフレームをグループ化した結果を表します。
        for depth, df_group in obj_pd_grouped:
            #print(f"Depth: {depth}<br>")
            #print(f"Group.index: {df_group.index}<br>")
            dict_station_TMP[depth] = df_group.index.tolist()
        #exit()
        
        ### Delete SampleID according to the reads sheet columns
        dict_depth = OrderedDict()
        for depth, list_sampleIDs  in dict_station_TMP.items():
            #print("depth", depth, "<br>")
            #print("list_sampleIDs", list_sampleIDs, "<br>")
            list_sampleID_selected = []
            for sampleID in list_sampleIDs:
                if sampleID in df_reads.columns.tolist():
                    list_sampleID_selected.append(sampleID)
            dict_depth[depth] = list_sampleID_selected

        # 新しいデータフレームを作成
        df_reads_new = pd.DataFrame()
        for depth, list_sampleIDs  in dict_depth.items():
            #print("depth", depth, "<br>")
            if len(list_sampleIDs):
                #print("list_sampleIDs", list_sampleIDs, "<br>")
                #df_reads_new[depth] = df_reads[list_sampleIDs].sum(axis=1)
                df_reads_new[depth] = (df_reads[list_sampleIDs] > 0).sum(axis=1)
        # Target 列を df_reads_new に加える
        df_reads_new['Target'] = df_reads['Target']

        #### Printout for making sure
        #df_reads_new.to_csv(eachDirAddress + f"210_df_reads_{cruiseName}_depth.csv")
        
        ## 格納
        dct_dfs = OrderedDict()
        dct_dfs["reads"] = df_reads_new
        dct_dfs["environments"] = df_envis

        list_dfs_cruises_depths_fn.append([cruiseName, name_excelFile, dct_dfs, binary_or_not])

    #print("### Exit point 3408 ###<br>")
    #exit()

    return list_dfs_cruises_depths_fn


def delete_columns_with_all0():
    #print("### delete_columns_with_all0() ###<br>")

    list_dfs_cruises_excelFiles_0columnsDeleted = []

    for rec in list_dfs_cruises:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dic_df = rec[2]
        df_reads = dic_df["reads"]
        df_envis = dic_df["environments"]
        
        list_column_to_drop = []
        for col in df_reads.columns:
            if col == "Target": continue
            sum_col = df_reads[col].sum()
            #print("col", col, "<br>")
            #print("sum_col", sum_col, "<br>")
            if sum_col < 1:
                list_column_to_drop.append(col)
                #exit()
        #print("list_column_to_drop", list_column_to_drop, "<br>")
        #print("df_reads", df_reads.shape, "<br>")
        df_reads_dropped = df_reads.drop(columns=list_column_to_drop)
        #print("df_reads_dropped", df_reads_dropped.shape, "<br>")

        dic_df2 = OrderedDict()
        dic_df2["reads"] = df_reads_dropped
        dic_df2["environments"] = df_envis
        list_dfs_cruises_excelFiles_0columnsDeleted.append([cruiseName, name_excelFile, dic_df2])
    
    return list_dfs_cruises_excelFiles_0columnsDeleted


def merge_severalCruseSeveralDFs_to_1df(list_dfs_fn):
    #print("### merge_severalCruseSeveralDFs_to_1df() ###")
    #print("list_dfs_fn length:", len(list_dfs_fn))
    #for rec in list_dfs_fn:
    #    print("rec keys:", rec[2].keys() if len(rec) > 2 else "Invalid record")

    list_dfs_reads = []
    list_dfs_envis = []
    ##for rec in list_dfs_cruises_excelFiles_0columnsDeleted:
    for rec in list_dfs_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dic_df = rec[2]
        binary_or_not = rec[3]
        #print("cruiseName", cruiseName, "<br>")
        #print("name_excelFile", name_excelFile, "<br>")
        #print("binary_or_not", binary_or_not, "<br><br>")
        df_reads = dic_df["reads"]
        list_dfs_reads.append(df_reads)
        df_environments = dic_df["environments"]
        list_dfs_envis.append(df_environments)
        #print("name_excelFile", name_excelFile, "<br>")
        #fileNameR = eachDirAddress + "180_" + cruiseName + "_" + name_excelFile + "_reads.csv"
        #df_reads.to_csv(fileNameR)
        #df_reads.to_csv(eachDirAddress + f"170_reads_merged_{cruiseName}.csv")
        #df_environments.to_csv(eachDirAddress + f"170_envis_concat_{cruiseName}.csv")  # 132 lines

    #exit()
    #for df in list_dfs_reads:
    #    print("df<br>")
    #    for name_column in df.columns:
    #        print('name_column', name_column, "<br>")
    #exit()

    df_reads_merged_TMP = reduce(lambda left, right: pd.merge(left, right, on='Target', how='outer'), list_dfs_reads)
    df_reads_merged_TMP = df_reads_merged_TMP.set_index("Target")
    #print('df_reads_merged_TMP.columns', df_reads_merged_TMP.columns, "<br>")
    #exit()
    df_reads_merged = df_reads_merged_TMP.fillna(0)
    #print('df_reads_merged.columns', df_reads_merged.columns, "<br>")
    #exit()

    #print("len(list_dfs_envis)", len(list_dfs_envis), "<br>")
    df_envis_concat_TMP = pd.concat(list_dfs_envis, axis=0) # axis=0 は行方向に結合することを意味します（デフォルトの設定です）。
    #df_envis_concat_TMP.to_csv(eachDirAddress + "176_df_envis_concat_TMP.csv")
    #print("df_envis_concat_TMP.shape[0]:", df_envis_concat_TMP.shape[0])

    ## 重複を削除する
    #df_envis_concat1 = df_envis_concat_TMP.drop_duplicates()
    ##df_envis_concat1.to_csv(eachDirAddress + "176_df_envis_concat.csv")
    #print("df_envis_concat1.shape[0]:", df_envis_concat1.shape[0])
    #exit()
    df_envis_concat1 = df_envis_concat_TMP

    #print("list_dfs_reads[0].columns", list_dfs_reads[0].columns, "<br>")
    #exit()
    #df_reads_merged = pd.merge(list_dfs_reads[0], list_dfs_reads[1], on='Target', how='left')
    #df_reads_merged.to_csv(eachDirAddress + "180_reads_merged.csv")
    #df_envis_concat1.to_csv(eachDirAddress + "180_envis_concat.csv")
    #print("df_reads_merged", df_reads_merged, "<br>")
    #print("di_envis_concat", di_envis_concat, "<br>")
    
    #print("### Exit point 3565 ###<br>")
    #exit()

    #except Exception as e:
    #    raise ValueError(f"[正規表現エラー] {str(e)} (location: plot_results_by_gmt/re.search)")

    return df_reads_merged, df_envis_concat1


def merge_severalCruseSeveralDFs_to_1df_depth(list_dfs_depth_fn):
    #print("### merge_severalCruseSeveralDFs_to_1df_depth() ###<br>")

    list_dfs_reads = []
    list_dfs_envis = []
    ##for rec in list_dfs_cruises_excelFiles_0columnsDeleted:
    for rec in list_dfs_depth_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dic_df = rec[2]
        binary_or_not = rec[3]
        #print("cruiseName", cruiseName, "<br>")
        #print("name_excelFile", name_excelFile, "<br>")
        #print("binary_or_not", binary_or_not, "<br><br>")
        df_reads = dic_df["reads"]
        list_dfs_reads.append(df_reads)
        df_environments = dic_df["environments"]
        list_dfs_envis.append(df_environments)
        #print("name_excelFile", name_excelFile, "<br>")
        #fileNameR = eachDirAddress + "180_" + cruiseName + "_" + name_excelFile + "_reads.csv"
        #df_reads.to_csv(fileNameR)

    #exit()
    #for df in list_dfs_reads:
    #    print("df<br>")
    #    for name_column in df.columns:
    #        print('name_column', name_column, "<br>")
    #exit()

    df_reads_merged_TMP = reduce(lambda left, right: pd.merge(left, right, on='Target', how='outer'), list_dfs_reads)
    df_reads_merged_TMP = df_reads_merged_TMP.set_index("Target")
    df_reads_merged = df_reads_merged_TMP.fillna(0)
    #print('df_reads_merged.columns', df_reads_merged.columns, "<br>")
    #exit()

    df_envis_concat_TMP = pd.concat(list_dfs_envis, axis=0)
    df_envis_concat = df_envis_concat_TMP.drop_duplicates()

    #print("list_dfs_reads[0].columns", list_dfs_reads[0].columns, "<br>")
    #exit()
    #df_reads_merged = pd.merge(list_dfs_reads[0], list_dfs_reads[1], on='Target', how='left')
    #df_reads_merged.to_csv(eachDirAddress + "180_reads_merged.csv")
    #di_envis_concat.to_csv(eachDirAddress + "180_envis_concat.csv")
    #print("df_reads_merged", df_reads_merged, "<br>")
    #print("di_envis_concat", di_envis_concat, "<br>")
    #exit()

    #print("### Exit point 3554 ###<br>")
    #exit()
    #except Exception as e:
    #    raise ValueError(f"[正規表現エラー] {str(e)} (location: plot_results_by_gmt/re.search)")

    return df_reads_merged, df_envis_concat


def change_strings_to_int_in_df(list_dfs_cruises_excelFiles_fn):
    #print("### change_strings_to_int_in_df() ###\n")
    list_dfs_cruises_excelFiles_mod = []
    for rec in list_dfs_cruises_excelFiles_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]

        dic_df2 = OrderedDict()
        # 整数列を int 型に変換
        for col in df_reads.columns:
            #print("col:", col, "<br>")
            #print("dtype:", df_reads[col].dtype, "<br>")
            if df_reads[col].dtype == 'int64':
                df_reads[col] = df_reads[col].astype(int)
                #print("dtype2:", df_reads[col].dtype, "<br>")
            #print("<br>")

        dic_df2["reads"] = df_reads
        dic_df2["environments"] = df_envis
        list_dfs_cruises_excelFiles_mod.append([cruiseName, name_excelFile, dic_df2])

    return list_dfs_cruises_excelFiles_mod


def delete_control(list_dfs_cruises_excelFiles_fn):
    #print("### delete_control() ###<br>")
    #print("use_control", use_control, "<br>")
    list_dfs_cruises_excelFiles_mod = []
    for rec in list_dfs_cruises_excelFiles_fn:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]
        
        #print("name_excelFile", name_excelFile, "<br>")
        
        indexObject_sampleID_control = df_envis[df_envis['Station'] == 'Control'].index
        list_sampleID_control = indexObject_sampleID_control.tolist()
        #print("list_sampleID_control", list_sampleID_control, "<br>")
        df_reads_new = df_reads.drop(columns=list_sampleID_control)

        dic_df2 = OrderedDict()
        dic_df2["reads"] = df_reads_new
        dic_df2["environments"] = df_envis
        list_dfs_cruises_excelFiles_mod.append([cruiseName, name_excelFile, dic_df2, binary_or_not])

    return list_dfs_cruises_excelFiles_mod

def add_sampleID_cruse_depth(list_dfs_cruises):
    #print("### Confirmation: 010 list_dfs_cruises ###<br>")
    list_dfs_cruises_excelFiles_mod = []
    for rec in list_dfs_cruises:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]

        #df_reads_newName = df_reads
        list_column_new = []
        for column_reads in df_reads.columns.to_list():
            if column_reads == "Target":
                #print("Target end")
                list_column_new.append(column_reads)
                break
            cruise = df_envis.loc[column_reads, 'Cruise']
            station = df_envis.loc[column_reads, 'Station']
            depth = df_envis.loc[column_reads, 'Depth']
            if isinstance(depth, (int, float)):
                list_column_new.append(cruise + "_" + column_reads + "_" + station + "_" + str(depth) + "m")
            else:
                list_column_new.append(cruise + "_" + column_reads + "_" + station + "_" + str(depth))
        #print("list_column_new", list_column_new, "<br>")
        df_reads_newName = df_reads.copy()
        df_reads_newName.columns = list_column_new

        ### df_reads_newName を確認
        #print("df_reads_newName<br>")
        #print(df_reads_newName.columns.to_list(), "<br>")
        #for index, row in df_reads_newName.iterrows():
        #    print(f"Index: {index}<br>")
        #    print("row.values", row.values, "<br>")
        #print("<br>")
        #print("df_reads2<br>")
        #print(df_reads.columns.to_list(), "<br>")
        #for index, row in df_reads.iterrows():
        #    print(f"Index: {index}<br>")
        #    print("row.values", row.values, "<br>")
        #print("<br>")
        #exit()
        
        dic_df2 = OrderedDict()
        dic_df2["reads"] = df_reads_newName
        dic_df2["environments"] = df_envis
        list_dfs_cruises_excelFiles_mod.append([cruiseName, name_excelFile, dic_df2, binary_or_not])
        
    return list_dfs_cruises_excelFiles_mod


def add_station_cruise(list_dfs_cruises_stations):
    #print("### Confirmation: 010 list_dfs_cruises ###<br>")
    list_dfs_cruises_mod = []
    for rec in list_dfs_cruises_stations:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]

        list_column_new = []
        #print("df_reads.columns.to_list()", df_reads.columns.to_list(), "<br>")
        for column_station_reads in df_reads.columns.to_list():
            if column_station_reads == "Target":
                #print("Target end")
                list_column_new.append(column_station_reads)
                break
            cruiseName_envis = df_envis.loc[df_envis['Station'] == column_station_reads, 'Cruise'].values[0]
            #print("cruiseName_envis", cruiseName_envis, "<br>")
            # このコードでは、df.loc[df['名前'] == 'Bob', '職業'] で「名前」が 'Bob' の行の「職業」列を選択し、.values[0] でその値を取り出しています。
            list_column_new.append(cruiseName_envis + "_" + column_station_reads)
        df_reads_newName = df_reads.copy()
        df_reads_newName.columns = list_column_new

        ## df_reads_newName を確認
        #print("df_reads_newName<br>")
        #print(df_reads_newName.columns.to_list(), "<br>")
        #for index, row in df_reads_newName.iterrows():
        #    print(f"Index: {index}<br>")
        #    print("row.values", row.values, "<br>")
        #print("<br>")
        #exit()
        
        dic_df2 = OrderedDict()
        dic_df2["reads"] = df_reads_newName
        dic_df2["environments"] = df_envis
        list_dfs_cruises_mod.append([cruiseName, name_excelFile, dic_df2, binary_or_not])
        
    return list_dfs_cruises_mod


def making_fundamental_dataframes(eachDirAddress, input_file_userDB, database_address):
    #print("### making_fundamental_dataframes() ###")

    ## セッションの全キーと値を一覧表示
    #for key, value in session.items():
    #    print(f"{key}: {value}")
    #print("### abort() 3797 ###")
    #abort(400)
    #input_file_userDB_filename = get_session_param('input_file_userDB')
    use_control = get_session_param('use_control')
    list_cruiseNames = get_session_param('list_cruiseNames')
    ASV_detection_criteria = get_session_param('ASV_detection_criteria')
    sitename_map = get_session_param('sitename_map')

    #print("#### list_cruiseNames", list_cruiseNames, "######")



    #print("### making_fundamental_dataframes ###<br>")
    #print("list_cruiseNames", list_cruiseNames, "<br>")
    #exit()

    #print("1111 input_file_userDB: ", input_file_userDB)
    #exit()
    if input_file_userDB:
        if input_file_userDB.filename.endswith('.xlsx'):
            new_filename = '000_user.xlsx'
            file_path = os.path.join(eachDirAddress, new_filename)
            #print("file_path", file_path)
            #exit()
            with open(file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file_userDB.stream, output_file)
        elif input_file_userDB.filename.endswith('.csv'):
            new_filename = '000_user.csv'
            file_path = os.path.join(eachDirAddress, new_filename)
            with open(file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file_userDB.stream, output_file)
        elif input_file_userDB.filename.endswith('.txt'):
            new_filename = '000_user.txt'
            file_path = os.path.join(eachDirAddress, new_filename)
            with open(file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file_userDB.stream, output_file)
        else:
            print("Error: A valid .xlsx/.csv file has not been uploaded.")
            exit()
    #elapsed_time_uploade = round((time.time() - startTime),1)
    #print("解析にかかった時間: {0}".format(elapsed_time_uploade) + " 秒.<br>")

    #print("### get_environments_reads_as_df ###<br>")
    list_dfs_cruises_excelFiles_TMP = get_environments_reads_as_df(eachDirAddress, list_cruiseNames, database_address)

    check_dfs(list_dfs_cruises_excelFiles_TMP)
    #print("list_dfs_cruises_excelFiles_TMP")
    #print("")
    #exit()

    list_dfs_cruises_excelFiles_TMP = add_binaruy_or_not(list_dfs_cruises_excelFiles_TMP)

    #list_dfs_cruises_excelFiles_TMP = change_strings_to_int_in_df(list_dfs_cruises_excelFiles_TMP)
    
    #print("use_control", use_control, "<br>")
    if use_control == "delete":
        list_dfs_cruises_excelFiles_TMP = delete_control(list_dfs_cruises_excelFiles_TMP)
    #print("### Confirmation: delete_control ###<br>")
    #for rec in list_dfs_cruises_excelFiles_TMP:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    df_reads = dict_df["reads"]
    #    print("cruiseName",cruiseName, "<br>")
    #    print("name_excelFile",name_excelFile, "<br>")
    #    df_reads.to_csv(eachDirAddress + f"500_{cruiseName}_df_reads.csv")
    ##print("### abort point 3861 ###")
    ##abort(400)

    list_dfs_cruises_excelFiles_TMP = merge_ASV_2_Species(list_dfs_cruises_excelFiles_TMP)
    #print("### Confirmation: merge_ASV_2_Species ###<br>")
    #for rec in list_dfs_cruises_excelFiles_TMP:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    print("cruiseName",cruiseName, "<br>")
    #    print("name_excelFile",name_excelFile, "<br>")
    #    print("binary_or_not",binary_or_not, "<br>")
    #    df_reads.to_csv(eachDirAddress + f"510_{cruiseName}_df_reads_spMerged.csv")
    #print("### exit point 3887 ###")
    #exit()

    list_dfs_cruises = merge_oneCruseSeveralDFs_to_1df(list_dfs_cruises_excelFiles_TMP)
    #print("### Confirmation: 020 merge_oneCruseSeveralDFs_to_1df ###<br>")
    #print("eachDirAddress", eachDirAddress, "<br>")
    #for rec in list_dfs_cruises:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    df_envis = dict_df["environments"]
    #    
    #    print("cruiseName", cruiseName)
    #    print("name_excelFile", name_excelFile)
    #    print("binary_or_not", binary_or_not)
    #    df_reads.to_csv(eachDirAddress + f"400_{cruiseName}_df_envis.csv")
    #    print("")
    #    #break
    ##exit()

    #list_dfs_cruises = changeName_Eng_EngJPN_reads(list_dfs_cruises)

    #print("### abort point 3912 ###")
    #abort(400)


    list_dfs_cruises = changeSpeciesName(list_dfs_cruises)
    #print("### Confirmation: changeSpeciesName ###<br>")
    #print("eachDirAddress", eachDirAddress, "<br>")
    #for rec in list_dfs_cruises:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    df_envis = dict_df["environments"]
    #    
    #    print("cruiseName", cruiseName)
    #    print("name_excelFile", name_excelFile)
    #    print("binary_or_not", binary_or_not)
    #    df_reads.to_csv(eachDirAddress + f"500_{cruiseName}_df_envis_changedSpName.csv")

    #    print("")
    #    #break
    #print("### Exit point analysis 3964")
    #exit()

    #print("### abort point 3930 ###")
    #abort(400)

    #print("ASV_detection_criteria", ASV_detection_criteria, "<br>")
    if ASV_detection_criteria > 1:
        list_dfs_cruises = exclude_lowReadOTU_readCount_to_ignore(list_dfs_cruises)

    #print("### Confirmation: exclude_lowReadOTU_readCount_to_ignore ###<br>")
    #print("eachDirAddress", eachDirAddress, "<br>")
    #for rec in list_dfs_cruises:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    df_reads = dict_df["reads"]
    #    df_envis = dict_df["environments"]
    #    
    #    print("cruiseName", cruiseName, "<br>")
    #    print("name_excelFile", name_excelFile, "<br>")
    #    print("binary_or_not", binary_or_not, "<br>")
    #    print("<br>")
    #    #break
    #exit()

    #print("### abort point 3961 ###")
    #abort(400)


    list_dfs_cruises_stations = merge_depth_to_station(list_dfs_cruises)
    #print("### Confirmation: merge_depth_to_station ###<br>")
    #print("eachDirAddress", eachDirAddress, "<br>")
    #for rec in list_dfs_cruises_stations:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    print("cruiseName", cruiseName, "<br>")
    #    print("binary_or_not", binary_or_not, "<br><br>")


    #    df_reads = dict_df["reads"]
    #    
    #    #print("cruiseName", cruiseName, "<br>")
    #    #for name_column in df_reads.columns:
    #    #    print("name_column", name_column, "<br>")
    #    #exit()
    #    
    #    #df_reads.to_csv(eachDirAddress + f"500_{cruiseName}_df_reads_station.csv")
    #    # Target 列を index にして転置
    #    df_reads_TMP = df_reads.set_index('Target')
    #    df_reads_transposed = df_reads_TMP.transpose()
    #    #df_reads_transposed.to_csv(eachDirAddress + f"500_{cruiseName}_df_reads_stationT.csv")

    #    df_envis = dict_df["environments"]
    #    #df_envis.to_csv(eachDirAddress + f"500_{cruiseName}_df_envis_depth.csv")


    list_dfs_cruises_depths = merge_station_to_depth(list_dfs_cruises, eachDirAddress)
    #print("### Confirmation: merge_station_to_depth ###<br>")
    #print("eachDirAddress", eachDirAddress, "<br>")
    #for rec in list_dfs_cruises_depths:
    #    cruiseName = rec[0]
    #    name_excelFile = rec[1]
    #    dict_df = rec[2]
    #    binary_or_not = rec[3]
    #    print("cruiseName", cruiseName, "<br>")
    #    print("binary_or_not", binary_or_not, "<br><br>")


    #    df_reads = dict_df["reads"]
    #    
    #    #print("cruiseName", cruiseName, "<br>")
    #    #for name_column in df_reads.columns:
    #    #    print("name_column", name_column, "<br>")
    #    #exit()
    #    
    #    df_reads.to_csv(eachDirAddress + f"510_{cruiseName}_df_reads_depth.csv")
    #    # Target 列を index にして転置
    #    df_reads_TMP = df_reads.set_index('Target')
    #    df_reads_transposed = df_reads_TMP.transpose()
    #    df_reads_transposed.to_csv(eachDirAddress + f"510_{cruiseName}_df_reads_depthT.csv")

    #    df_envis = dict_df["environments"]
    #    df_envis.to_csv(eachDirAddress + f"510_{cruiseName}_df_envis_depth.csv")
    #print("#### Exit point 3700 ####<br>")
    #exit()

    #print("### abort point 4010 ###")
    #abort(400)

    return list_dfs_cruises, list_dfs_cruises_stations, list_dfs_cruises_depths

