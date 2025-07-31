#!/bin/bash

echo "🧹 Deleting .pyc files..."
find . -name "*.pyc" -delete

echo "🛑 Stopping uWSGI..."
if [ -f /tmp/eDNAmap.pid ]; then
    uwsgi --stop /tmp/eDNAmap.pid
    echo "✅ uWSGI stopped via PID file."
    sleep 2
else
    echo "⚠️ PID file not found. Attempting to kill uWSGI manually..."
fi

# 念のためすべての uwsgi プロセスを停止
pkill -f 'uwsgi --ini wsgi.ini'
sleep 2

echo "🚀 Starting uWSGI with wsgi.ini..."
uwsgi --ini wsgi.ini &

echo "✅ uWSGI restarted. Check /var/log/uwsgi/eDNAmap.log for details."


## 起動後に以下のコマンドでプロセス数を確認
## ps aux | grep 'uwsgi --ini wsgi.ini' | grep -v grep

