Flask Interface for CeviDB-Tool
===============================

This tool provides a webinterface for the cevidbtool.
Using a webinterface simplifies maintenance and reduces
the support needed for new regions wanting to use the tool.

Setup Debian
------------
  - Install Flask and all dependencies via apt
  - clone this repo into `/var/www/db2excel_flask`
  - symlink:
    - `/usr/share/javascript/bootstrap4` to `dbtool/static/bootstrap`
    - `/usr/share/javascript/jquery` to `dbtool/static/jquery`
  - setup apache2 vhost `db2excel` with pointing to `/var/www/db2excel_flask/wsgi/db2excel.wsgi`
  - add cronjob for www-data `*/5  *  *  *  * cronic wget -q -O/dev/null db2excel.ceviregionzuerich.ch/cleanup`
    (output to `/dev/null` needed, as wget can not store returned file)

Dependencies
------------
(probably incomplete)
  - python3-openpyxl
  - python3-flaskext.wtf

