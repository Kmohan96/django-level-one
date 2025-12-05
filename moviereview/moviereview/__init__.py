import pymysql
pymysql.install_as_MySQLdb() 


#python manage.py shell -c "from django.db import connection; c=connection.cursor(); c.execute('SELECT DATABASE(),VERSION()'); print(c.fetchone())"