from flask import render_template, jsonify, abort
from datetime import date
from eDNAmap_analysis import making_fundamental_dataframes, plot_map_and_drow_figs
from flask import session
from utils.session_utils import get_session_param
import os
import pandas as pd
import numpy as np
import secrets
import string
import pickle

RESULT_FOLDER = 'results'

from flask import request

def convert_numeric_columns(list_dfs):
    list_dfs_converted = []
    for rec in list_dfs:
        cruiseName, name_excelFile, dict_df, binary_or_not = rec
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]

        # 数値列を float に変換（Target 列は除外）
        for col in df_reads.columns:
            if col != "Target":
                df_reads[col] = pd.to_numeric(df_reads[col], errors='coerce')

        dict_df["reads"] = df_reads
        list_dfs_converted.append([cruiseName, name_excelFile, dict_df, binary_or_not])
    return list_dfs_converted


def get_parameters_from_flask_request():
    #print("### get_parameters_from_flask_request() ###")
    #print("=== request.form contents ===")
    #for name, value in request.form.items():
    #    print(f"{name}: {value}")
    #print("=== request.files contents ===")
    #for name, file in request.files.items():
    #    print(f"{name}: {file.filename}")
    ##print("### Stop point 24 ###")
    ##abort(400)


    html_name = request.form.get("html_name")
    use_control = request.form.get("use_control", "delete")
    ASV_detection_criteria = int(request.form.get("ASV_detection_criteria", 1))
    ASV_comparison_criateria = int(request.form.get("ASV_comparison_criateria", 2))
    readFraction_to_ignore = request.form.get("readFraction_to_ignore", "0.1")
    inc_exclude_Nohit = request.form.get("inc_exclude_Nohit", "exclude")
    index_distance = request.form.get("index_distance", "jaccard")
    PDF_file = request.form.get("PDF_file", "create")
    sitename_map = request.form.get("sitename_map", "shown")

    # ファイルアップロード
    input_file_userDB = request.files.get("upload_file_excel")
    species_file = request.files.get("list_speciesName_pulldown")

    # 種名の取得
    if species_file and species_file.filename.endswith(".txt"):
        list_speciesName_pulldown = [
            f"^{line.strip()}$" for line in species_file.read().decode().splitlines()
        ]
    elif request.form.get("speciesName_window"):
        list_speciesName_pulldown = [
            s.strip() for s in request.form.get("speciesName_window").split(";")
        ]
    else:
        list_speciesName_pulldown = [request.form.get("speciesName_pulldown", "")]

    # クルーズ名
    list_cruiseNames = request.form.getlist("list_cruiseNames")
    if input_file_userDB and input_file_userDB.filename:
        if input_file_userDB.filename.endswith(".xlsx"):
            list_cruiseNames.insert(0, "User-xlsx")
        elif input_file_userDB.filename.endswith(".csv"):
            list_cruiseNames.insert(0, "User-csv")
        elif input_file_userDB.filename.endswith(".txt"):
            list_cruiseNames.insert(0, "User-txt")

    return (
        html_name, "SpeciesSearch", input_file_userDB, use_control,
        ASV_detection_criteria, ASV_comparison_criateria,
        readFraction_to_ignore, inc_exclude_Nohit, index_distance,
        PDF_file, list_cruiseNames, list_speciesName_pulldown, sitename_map
    )


def prepare_fundamental_dataframes(eachDirAddress):
    """
    与えられた list_cruiseNames に基づいて、基本的なデータフレーム群を生成する。
    Flask アプリから呼び出すためのラッパー関数。
    """

    list_dfs_cruises, list_dfs_cruises_stations, list_dfs_cruises_depths = making_fundamental_dataframes(eachDirAddress)
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
    #print("### abort point module.py 114 ###")
    #abort(400)

    return list_dfs_cruises, list_dfs_cruises_stations, list_dfs_cruises_depths


def load_oednamap_results(eachDirAddress, list_dfs_cruises):
    #print("### load_oednamap_results() ###")
    '''
    3 変数を return
        "species_list": species_list_2,
        "map_image": map_image,
        "depth_image": depth_image
    '''


    # ファイル名の定義
    map_image_filename = "150_map.png"
    depth_image_filename = "210_pheatmap_depth.png"

    # フルパスの作成
    map_image_path = os.path.join(eachDirAddress, map_image_filename)
    depth_image_path = os.path.join(eachDirAddress, depth_image_filename)

    # ファイルの存在確認
    map_image = map_image_filename if os.path.exists(map_image_path) else None
    print("module.py map_image", map_image)
    depth_image = depth_image_filename if os.path.exists(depth_image_path) else None


    ####################################
    ### species_list = [] の作成

    #print("### Confirmation3: list_dfs_cruises ###")
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
    #    df_reads.to_csv(f"{eachDirAddress}3333_df_{cruiseName}_reads.csv")
    #    df_envis.to_csv(f"{eachDirAddress}3333_df_{cruiseName}_envis.csv")
    #print("### abort module.py line 141 ###")
    #abort(400)

    species_list_2 = []
    #print("### making new species_list  ###")
    for rec in list_dfs_cruises:
        cruiseName = rec[0]
        name_excelFile = rec[1]
        dict_df = rec[2]
        binary_or_not = rec[3]
        df_reads = dict_df["reads"]
        df_envis = dict_df["environments"]
        #print("cruiseName", cruiseName)

        for sample_id in df_reads.columns:

            if sample_id == "Target":
                break
            #print("sample_id", sample_id)
            df_reads[sample_id] = pd.to_numeric(df_reads[sample_id], errors='coerce')
            df_reads_only2_TMP = df_reads[[sample_id, 'Target']]
            df_reads_only2 = df_reads_only2_TMP.sort_values(by=sample_id, ascending=False)

            detected_species = []
            for index, row in df_reads_only2.iterrows():
                reads = row.iloc[0]
                species = row.iloc[1]
                #print(f"read: {reads}, species: {species}")
                if reads > 0:
                    detected_species.append({
                        "name": species,
                        "common_name": "NA",
                        "reads": int(reads)
                    })
            species_list_2.append({
                "cruise": cruiseName,
                "sample_id": sample_id,
                "detected_species": detected_species
            })

    #print("### abort module.py line 184 ###")
    #abort(400)

    return {
        "species_list": species_list_2,
        "map_image": map_image,
        "depth_image": depth_image
    }



def prepare_result_directory(count_file: str) -> tuple[str, str]:
    #print("### prepare_result_directory() ###")
    # count.dat の読み込みと次の ID の決定
    if not os.path.exists(count_file):
        with open(count_file, 'w', encoding='utf-8') as f:
            f.write('0: 1970-01-01\n')
    with open(count_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    last_line = lines[-1] if lines else '0: 1970-01-01'
    dirName_count = int(last_line.split(':')[0].strip())

    # ランダムID生成
    rand_str = ''.join(secrets.choice(string.ascii_letters) for _ in range(6))
    dirname_rand = f"{dirName_count}-{rand_str}"
    eachDirAddress = os.path.join(RESULT_FOLDER, dirname_rand)
    eachDirAddress = eachDirAddress + "/"
    #print("eachDirAddress", eachDirAddress)
    #print("### abort() module.py 137 ###")
    #abort(400)
    os.makedirs(eachDirAddress, exist_ok=True)

    # count.dat に次のIDを追記
    next_id = dirName_count + 1
    today_str = date.today().isoformat()
    with open(count_file, 'a', encoding='utf-8') as f:
        f.write(f"{next_id}: {today_str}\n")

    return dirname_rand, eachDirAddress, dirName_count, dirname_rand


def build_result_html(dirname_rand, eachDirAddress, list_dfs_cruises):
    #print("### build_result_html() ###")
    result_data = load_oednamap_results(eachDirAddress, list_dfs_cruises)

    list_cruiseNames = get_session_param('list_cruiseNames')
    list_speciesName_pulldown = get_session_param('list_speciesName_pulldown')
    #list_speices_fewTimeDetect = pickle.loads(session['list_speices_fewTimeDetect'])
    list_sampleID_all0 = pickle.loads(session['list_sampleID_all0'])
    ASV_comparison_criateria = pickle.loads(session['ASV_comparison_criateria'])

    # ここで CSV を読み込む
    df_4_R_reads = pd.read_csv(os.path.join(eachDirAddress, "200_communityData4R.csv"), index_col=0)
    df_4_R_reads_station = pd.read_csv(os.path.join(eachDirAddress, "200_communityData4R_station.csv"), index_col=0)
    
    # 画像ファイルの存在確認
    pheatmap_image_path = os.path.join(eachDirAddress, "210_pheatmap.png")
    pheatmap_station_image_path = os.path.join(eachDirAddress, "210_pheatmap_station.png")

    pheatmap_image = "210_pheatmap.png" if os.path.exists(pheatmap_image_path) else None
    pheatmap_station_image = "210_pheatmap_station.png" if (
        len(df_4_R_reads) != len(df_4_R_reads_station) and
        os.path.exists(pheatmap_station_image_path) and
        os.path.getsize(pheatmap_station_image_path) > 0
    ) else None

    return render_template(
        'result.html',
        dirname_rand = dirname_rand,
        list_cruiseNames = list_cruiseNames,
        list_speciesName_pulldown = list_speciesName_pulldown,
        #len_list_speices_fewTimeDetect = len(list_speices_fewTimeDetect),
        len_list_sampleID_all0 = len(list_sampleID_all0),
        #ASV_comparison_criateria=1,
        ASV_comparison_criateria = ASV_comparison_criateria,
        map_image = result_data["map_image"],
        depth_image = result_data["depth_image"],
        species_list = result_data["species_list"],
        df_4_R_reads = df_4_R_reads,
        df_4_R_reads_station = df_4_R_reads_station,
        pheatmap_image=pheatmap_image,
        pheatmap_station_image=pheatmap_station_image

    )

def run_analysis(dirname_rand: str, eachDirAddress: str) -> str:
    #print("### run_analysis() ###", flush=True)

    os.makedirs(eachDirAddress, exist_ok=True)

    plot_map_and_drow_figs(eachDirAddress)
    compression()
    return os.path.join(eachDirAddress, "300_results.html")


def compression():
    # 出力ディレクトリをZIP圧縮する処理（簡易版）
    pass
