#!/bin/bash

#plasma_store -m 100000000 -s /tmp/plasma &
#sleep 1

if $(python --version | grep "Python 3" > /dev/null); then
  echo "PYTHON points to python3"
  PYTHON=python
else
  echo "PYTHON points to python"
  PYTHON=python3
fi

echo "PYTHON=$PYTHON"

# initial fetch
$PYTHON fetcher/run.py -c 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv' -e 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
# start cron to trigger fetch every minute
cron

$PYTHON src/run.py
