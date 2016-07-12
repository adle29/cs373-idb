psql -c "drop database golazo_dev;"
createdb golazo_dev
rm -r migrations
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
python3 scrape.py
