###  initialization
1. set a mysql enviornment.
2. get a youtube api key.
3. make a config.json file based on config_form.json file.
4. install required packages: ```pip install -r requirements.txt```
5. create a database: ```python3 create_database.py```
6. register at crontab: ```*/20 * * * * cd [**PATH**]; source ./venv/bin/activate; python3 record.py```