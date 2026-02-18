# eDNAmap
A Web Tool/Database for Metabarcodes in the Northwestern Pacific and Beyond


---

## Analysis site

<!-- CGI: Fast   -->
yurai (CGI: fast)   
[https://yurai.aori.u-tokyo.ac.jp/eDNAmap](https://yurai.aori.u-tokyo.ac.jp/eDNAmap)   
(
[https://oedna.opensci.aori.u-tokyo.ac.jp/eDNAmap/](https://oedna.opensci.aori.u-tokyo.ac.jp/eDNAmap/) or [https://opensci.aori.u-tokyo.ac.jp/eDNAmap/](https://opensci.aori.u-tokyo.ac.jp/eDNAmap/))   
(Since 24 Mar. 2025)   

os3 (CGI: slow)   
[https://133.167.89.139/eDNAmap/index.1.0.1.html](https://133.167.89.139/eDNAmap/index.1.0.1.html)   
(Since 2 Dec. 2025)   

viento (FLASK: medium)   
[https://orthoscope.jp/eDNAmap](https://orthoscope.jp/eDNAmap)   
(Since 23 July 2025)      


---
## Instruction　　　
[https://fish-evol.org/eDNAmap_instruction/index.html](https://fish-evol.org/eDNAmap_instruction/index.html)   

---
## Programming code　　　
The programming code is available from [Releases](https://github.com/jun-inoue/eDNAmap/releases/tag/v1.0.0).  A user can install eDNAmap on a web server as follows:
- Save downloaded html and cgi-bin directories in /var/www/.
- Install R and the package,[vegan](https://cran.r-project.org/web/packages/vegan/index.html).
- Install Pandas by running the following command in a Python environment: pip install pandas.
- Save the dowlonaded [Generic Mapping Tools](https://www.generic-mapping-tools.org) in the /cgi-bin/EDNAMAPscripts100 directory.   

Those scripts were confirmed to run on the Linux operating system with an Apache HTTP Server Server.   

<!-- 
---

## Deployment and Maintenance

### uWSGI Restart Script

To restart the uWSGI server and clear Python cache files, use the provided script:   
bash restart_uwsgi.sh   
This script performs the following steps:   
Deletes all .pyc files in the project directory.   
Stops uWSGI using the PID file (/tmp/eDNAmap.pid) if it exists.   
Kills any remaining uWSGI processes as a fallback.   
Restarts uWSGI using the wsgi.ini configuration file.   
Log output can be checked at /var/log/uwsgi/eDNAmap.log.   
-->

---
## Citation
Inoue, J. et al.   
eDNAmap: A Metabarcoding Web Tool for Comparing Marine Biodiversity, with Special Reference to Teleost Fish. Manuscript submitted for publication.   

---
## Contact 
Email: [_jinoueATg.ecc.u-tokyo.ac.jp_](http://www.fish-evol.org/index_eng.html)
<br />  
