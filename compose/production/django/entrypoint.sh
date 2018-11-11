#!/bin/sh

set -o errexit
set -o nounset


cmd="$@"



sqlserver_ready() {
python3 << END
import sys

import pyodbc
server = 'mssql'
database = 'golfcapture'
username = 'sa'
password = 'g0lfc@pture'

print('xxxxxxyyyyyyyzzzzzz')

try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';PORT=1433;DATABASE=master;UID='+username+';PWD='+ password)
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    print(cursor)
    sqlcommand = "if db_id('golfcapture') is  null CREATE DATABASE golfcapture;"
    cursor.execute(sqlcommand)
    cursor.commit()
    cnxn.commit()

except Exception as inst:
        cursor.rollback()
        cursor.close()
        print (type(inst))
        print (inst.args)
        print (inst)


sys.exit(0)

END
}

until sqlserver_ready; do
  >&2 echo 'Sql Server is unavailable (sleeping)...'
  sleep 1
done

>&2 echo 'Sql Server is up - continuing...'


exec $cmd
