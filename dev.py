from app import app

if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)

# (venv) [inouejun:ednamap]$ python3 dev.py 
# http://127.0.0.1:5000/ednamap
# アドレスの最後に / を入れないこと。