import sys
sys.path.insert(0, '/var/www/db2excel_flask')

from dbtool import create_app
application = create_app()
