current_path=`pwd`
sqlite3 $current_path/instance/flaskr.sqlite "update chat set deleted=1 where random()<0.5 and deleted=0"