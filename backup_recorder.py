from utils.get_config import config
import os

passwd = config['database']['passwd']
cmd = f"mysqldump -u root -p{passwd!r} {config['database']['database']} > backup.sql 2>/dev/null"
os.system(cmd)