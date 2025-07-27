#nohup rsync --rsh="ssh -p 10022" app.py jinoue@157.82.133.212:/home/jinoue/oednamap &
#nohup rsync --rsh="ssh -p 10022" eDNAmap_analysis.py jinoue@157.82.133.212:/home/jinoue/oednamap &
nohup rsync --rsh="ssh -p 10022" eDNAmap_module.py jinoue@157.82.133.212:/home/jinoue/oednamap &
#nohup rsync -avz -e "ssh -p 10022" templates jinoue@157.82.133.212:/home/jinoue/oednamap &
#nohup rsync -avz -e "ssh -p 10022" static jinoue@157.82.133.212:/home/jinoue/oednamap &
#nohup rsync -avz -e "ssh -p 10022" utils jinoue@157.82.133.212:/home/jinoue/oednamap &

#nohup rsync -avz app.py osadm@160.16.70.235:/home/osadm/oednamap &
#nohup rsync -avz eDNAmap_analysis.py osadm@160.16.70.235:/home/osadm/oednamap &
#nohup rsync -avz eDNAmap_module.py osadm@160.16.70.235:/home/osadm/oednamap &
#nohup rsync -avz templates osadm@160.16.70.235:/home/osadm/oednamap &
#nohup rsync -avz static osadm@160.16.70.235:/home/osadm/oednamap &
#nohup rsync -avz utils osadm@160.16.70.235:/home/osadm/oednamap &
