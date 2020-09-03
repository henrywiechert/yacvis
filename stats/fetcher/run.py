import os
import numpy as np
import pandas as pd
import argparse
import logging
from brain_plasma import Brain

# example file:
# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv

logger = logging.getLogger(__name__)
brain = Brain()


def setLogLevel(isDebugEnabled):
    if isDebugEnabled: logLevel = logging.DEBUG
    else:              logLevel = logging.INFO
    logging.basicConfig(format='%(asctime)s|%(levelname)s:%(message)s')
    logger.setLevel(logLevel)


def createArgsParser():
    logger.debug("Create Parser")
    parser = argparse.ArgumentParser(description='Fetch covid csv data from Johns Hopkins University Repo')
    parser.add_argument( '-f', '--file', help='input file name (perf/intel_pt trace)', metavar='<file>', required=True )
    parser.add_argument( '-d', '--debug', action="store_true", help='enable debug output' )
    parser.add_argument( '-D', '--dry-run', action="store_true", help='disable file creation' )
    return parser.parse_args()

def transform(df, indexer):
    # transpose -> columns are countries, rows are measurements
    df_t = df.T
    df_t = indexer(df, df_t)
    df_t = df_t.drop(['Province/State', 'Country/Region', 'Long', 'Lat'])
    # convert index to datetime
    df_t.index = pd.to_datetime(df_t.index)
    # add world column
    df_t['World'] = df_t.sum(axis=1)

    return df_t


def setIndex(df, df_t):
    df_t.columns = df['Country/Region'] + '/' + df['Province/State'].replace(np.NaN, '')
    return df_t


def setMultiIndex(df, df_t):
    # country/province as multi index (some countries have multiple provinces)
    multiIndex = pd.MultiIndex.from_arrays([df['Country/Region'], df['Province/State']])
    df_t.columns = multiIndex
    return df_t


def transformDataframe(df):
    df = transform(df, setIndex)
    return df


def transformDataframeMultiIndex(df):
    df = transform(df, setMultiIndex)
    return df


def storeDataframeIfNeeded(df):
    if brain.exists('df_covid'):
        if df.equals(brain['df_covid']):
            logger.info('No changes | Skip writing dataframe')
            return
        else:
            logger.info('Changes | Write dataframe to brain object')
    else:
        logger.info('No object | Write dataframe to brain object')

    brain['df_covid'] = df


def main():
    args = createArgsParser()
    setLogLevel(args.debug)

    url = args.file
    try:
        df = pd.read_csv(url)
    except:
        logger.error('Could not read URL {}', url)
        exit()
    else:
        df = transformDataframe(df)
        storeDataframeIfNeeded(df)

if __name__ == '__main__':
    main()
