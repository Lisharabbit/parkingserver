Features
---------

Installed apps:

* Django 2.0+
* MySQLdb or Psycopg2
* py.test_ and coverage setup
* PyYAML
* diff-match-patch
* django-cors-headers
* django-filter
* django-import-export
* djangorestframework
* et-xmlfile
* jdcal
* mysqlclient
* odfpy
* openpyxl
* pytz
* setuptools
* tablib

API URLs:

* GET:
``/parkdata/predict?streetMarker=`` followed by a valid street maker
* GET:
``/parkdata/lastweekdata?bayid=`` followed by a valid bayid
* POST:
 ``/parkdata/suggestbays``
Request fields:
 ``baylist period_m period_h``
 
Usage
-----

Create a Django project:



    mkdir parkingserver
    cd parkingserver
    
Run a Django server:


    python3 manage.py runserver
