from flask import Flask, session, render_template, request, jsonify, send_from_directory, redirect, abort
from flask_session import Session
from utils.session_utils import save_params_to_session
from datetime import timedelta
from utils.module import (
    run_analysis,
    prepare_result_directory,
    build_result_html,
    prepare_fundamental_dataframes,
    get_parameters_from_flask_request,
    convert_numeric_columns,
    compression
)
import os
import time
import pickle
import pandas as pd
import traceback

# .env 読み込み
from dotenv import load_dotenv
load_dotenv()

RESULT_FOLDER = 'results'
database_address = os.getenv("DATABASE_ADDRESS", "static/ASVtables/")
#filePass_English2Japanese, filePass_Sname2Cname = initialize_file_paths(database_address)

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/eDNAmap/static')


import redis
from flask_session import Session

# Redis セッション設定
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True  # ← 永続セッションを有効にする
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # ← 有効期限を設定
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379)

# セッションの初期化
Session(app)

# セキュアな secret_key を .env から取得
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_dev_key')
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/eDNAmap/debug')
def debug():
    list_dfs_cruises = pickle.loads(session['list_dfs_cruises'])
    df_reads = list_dfs_cruises[0][2]["reads"]
    html_table = df_reads.head().to_html()
    return render_template("debug.html", table=html_table)

@app.route('/ednamap')
@app.route('/ednamap/')
def redirect_to_eDNAmap():
    return redirect('/eDNAmap', code=302)

@app.route('/eDNAmap', methods=['GET'])
@app.route('/eDNAmap/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/eDNAmap/submit', methods=['POST'])
def submit():

    #print("request.form:", request.form)
    #print("request.files:", request.files)

    #print("### submit() ###", flush=True)

    start_time = time.time()

    ########################################################
    # フォームからの入力を取得
    #params = get_parameters_from_flask_request()
    try:
        params = get_parameters_from_flask_request()
    except SyntaxError as e:
        error_details = traceback.format_exc().replace('\n', '<br>')
        elapsed_time = round(time.time() - start_time, 1)
        return jsonify({
            'error': f'[SyntaxError] {str(e)}<br>{error_details}',
            'location': 'get_parameters_from_flask_request',
            'time': elapsed_time
        }), 400
    except ValueError as e:
        elapsed_time = round(time.time() - start_time, 1)
        return jsonify({
            'error': str(e),
            'location': 'get_parameters_from_flask_request',
            'time': elapsed_time
        }), 400



    #print("params", params)
    (
        html_name, searchType, input_file_userDB, use_control,
        ASV_detection_criteria, ASV_comparison_criteria,
        readFraction_to_ignore, inc_exclude_Nohit, index_distance,
        PDF_file, list_cruiseNames, list_speciesName_pulldown, sitename_map
    ) = params
    
    #print("app line 77 list_speciesName_pulldown", list_speciesName_pulldown)
    #exit()

    ## 各パラメータの中身を確認
    #print("=== DEBUG: sitename_map ===")
    #print("html_name:", html_name)
    #print("searchType:", searchType)
    #print("input_file_userDB:", input_file_userDB)
    #if not input_file_userDB or input_file_userDB.filename == '':
    #    print("input_file_userDB is empty or not uploaded.")
    #else:
    #    print("input_file_userDB filename:", input_file_userDB.filename)
    #print("use_control:", use_control)
    #print("ASV_detection_criteria:", ASV_detection_criteria)
    #print("##### ASV_comparison_criteria:", ASV_comparison_criteria)
    #abort(400)
    #print("readFraction_to_ignore:", readFraction_to_ignore)
    #print("inc_exclude_Nohit:", inc_exclude_Nohit)
    #print("index_distance:", index_distance)
    #print("PDF_file:", PDF_file)
    #print("list_cruiseNames:", list_cruiseNames)
    #print("list_speciesName_pulldown:", list_speciesName_pulldown)
    #print("sitename_map:", sitename_map)
    #print("===========================")
    #print("### Stop point 102 ###")
    ##return jsonify({'debug': 'Stopped for inspection'}), 200

    # 結果保存用ディレクトリの準備
    count_file = os.path.join(os.path.dirname(__file__), 'data', 'count.dat')
    dirname_rand, eachDirAddress, dirName_count, dirname_rand = prepare_result_directory(count_file)

    ########################################################
    # セッションに保存
    # 利用する場合は、例えば、input_file_userDB_filename = get_session_param('input_file_userDB')
    save_params_to_session({
        'html_name': html_name,
        'searchType': searchType,
        #'input_file_userDB': input_file_userDB.filename if input_file_userDB else None,
        'use_control': use_control,
        'ASV_detection_criteria': ASV_detection_criteria,
        'ASV_comparison_criteria': ASV_comparison_criteria,
        'readFraction_to_ignore': readFraction_to_ignore,
        'inc_exclude_Nohit': inc_exclude_Nohit,
        'index_distance': index_distance,
        'PDF_file': PDF_file,
        'list_cruiseNames': list_cruiseNames,
        'list_speciesName_pulldown': list_speciesName_pulldown,
        'sitename_map': sitename_map
    })

    # 現在の Flask セッションに保存されているすべてのキーと値を表示。
    #print("session keys and values:"), list(session.keys())
    #for key in session.keys():
    #    print(f"{key}: {pickle.loads(session[key])}")
    #return jsonify({'debug': 'Stopped for inspection'}), 200


    # DataFrames を生成してセッションに保存
    #print("list_cruiseNames1", list_cruiseNames)
    try:
        list_dfs_cruises, list_dfs_cruises_stations, list_dfs_cruises_depths = prepare_fundamental_dataframes(eachDirAddress, input_file_userDB, database_address)
        list_dfs_cruises = convert_numeric_columns(list_dfs_cruises)
        list_dfs_cruises_stations = convert_numeric_columns(list_dfs_cruises_stations)
        list_dfs_cruises_depths = convert_numeric_columns(list_dfs_cruises_depths)
        
        session['list_dfs_cruises'] = pickle.dumps(list_dfs_cruises)
        session['list_dfs_cruises_stations'] = pickle.dumps(list_dfs_cruises_stations)
        session['list_dfs_cruises_depths'] = pickle.dumps(list_dfs_cruises_depths)
        #print("DataFrame lists saved to session.")

    except FileNotFoundError as e:
        elapsed_time = round(time.time() - start_time, 1)
        return jsonify({
            'error': f'[DataFrame作成エラー] ファイルが見つかりません:<br>{str(e)}',
            'location': 'prepare_fundamental_dataframes',
            'time': elapsed_time
        }), 400
    except Exception as e:
        error_details = traceback.format_exc().replace('\n', '<br>')
        elapsed_time = round(time.time() - start_time, 1)
        return jsonify({
            'error': f'[DataFrame作成エラー] 予期しないエラー:<br>{error_details}',
            'location': 'prepare_fundamental_dataframes/general',
            'time': elapsed_time
        }), 500


    ########################################################
    # 分析の実行
    try:
        result_html_path = run_analysis(dirname_rand, eachDirAddress)

    except ValueError as e:
        elapsed_time = round(time.time() - start_time, 1)
        return jsonify({
            'error': f'[分析エラー] {str(e)}',
            'time': elapsed_time
        }), 200

    except Exception as e:
        error_details = traceback.format_exc().replace('\n', '<br>')
        elapsed_time = round(time.time() - start_time, 1)
        return jsonify({
            'error': f'[分析エラー] 予期しないエラー:<br>{error_details}',
            'location': 'run_analysis',
            'time': elapsed_time
        }), 500

    ########################################################
    # HTML結果の構築と保存
    result_html = build_result_html(dirName_count, dirname_rand, eachDirAddress, list_dfs_cruises, database_address)
    #print("result_html", result_html)
    result_path = os.path.join(eachDirAddress, "300_results.html")
    try:
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(result_html)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'location': 'build_result_html/write',
            'time': round(time.time() - start_time, 1)
        }), 500


    try:
        compression(eachDirAddress, dirName_count, list_cruiseNames, input_file_userDB, PDF_file, database_address)
    except Exception as e:
        error_details = traceback.format_exc()
        error_details_html = error_details.replace("\n", "<br>")
        elapsed_time = round(time.time() - start_time, 1)
        return jsonify({
            'error': f'[圧縮エラー] 予期しないエラー:<br>{error_details_html}',
            'location': 'compression',
            'time': elapsed_time
        })



    elapsed_time = round(time.time() - start_time, 1)
    
    # 結果のURLを返す
    #print("### return jsonify ###")
    return jsonify({
        'result_url': f'/eDNAmap/results/{dirname_rand}/300_results.html',
        'dirname_rand': dirname_rand,
        'time': elapsed_time
    })



# --- 静的ファイルの提供ルート ---
@app.route('/eDNAmap/results/<path:filename>')
def serve_result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    #app.run(debug=True, use_reloader=False)
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)

# Ubuntu24.04
# http://160.16.70.235:5000/eDNAmap
# Ubunt24.04 viento
# http://157.82.133.212:5000/eDNAmap
# Mac OS
# http://127.0.0.1:5001/eDNAmap
# 途中でストップさせたい場合。
# app.py
# return jsonify({'debug': 'Stopped for inspection'}), 200
# それ以外
# from flask import abort
# abort(400)  # または 403, 500 など適切なステータスコード

