./cloud_sql_proxy -dir=/cloudsql -instances=SH2020:us-east1:auto &
mysql -u lp -S /cloudsql/SH2020:us-east1:auto
