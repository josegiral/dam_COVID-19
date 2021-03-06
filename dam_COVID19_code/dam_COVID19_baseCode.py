import os
import numpy as np
import urllib
import zipfile
import datetime
from ipywidgets import widgets

import matplotlib.pylab as gr
small={'family' : 'normal','weight' : 'normal','size'   : 8}
medium={'family' : 'normal','weight' : 'normal','size'   : 10}
large={'family' : 'normal','weight' : 'bold','size'   : 13}
gr.rc('font', size=small['size'], weight='normal')          # controls default text sizes
gr.rc('axes', titlesize=medium['size'])     # fontsize of the axes title
gr.rc('axes', labelsize=medium['size'])    # fontsize of the x and y labels
gr.rc('xtick', labelsize=small['size'])    # fontsize of the tick labels
gr.rc('ytick', labelsize=small['size'])    # fontsize of the tick labels
gr.rc('legend', fontsize=small['size'])    # legend fontsize
gr.rc('figure', titlesize=large['size'])  # fontsize of the figure title

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# Example:
# inset_axes = inset_axes(parent_axes,
#                     width="30%", # width = 30% of parent_bbox
#                     height=1., # height : 1 inch
#                     loc=3)
# Indexing and gathering of data


import pandas as pd

def openCSV_DB(path,comp='zip',enc='latin-1'):
    data=pd.read_csv(path, compression=comp,encoding=enc)
    print('Data obtained from %s'%path)
    return data


def getCSSEGISandData(urlData=1):
    if urlData==1:
        localData=1-urlData
        srcDir='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

    if localData==1:
        srcDir='./Covid-19/csse_covid_19_data/csse_covid_19_time_series/'

    pathCases=srcDir+'time_series_covid19_confirmed_global.csv'
    pathDeaths=srcDir+'time_series_covid19_deaths_global.csv'
    pathRecov=srcDir+'time_series_covid19_recovered_global.csv'

    cases = openCSV_DB(path=pathCases,comp=None,enc='latin-1')
    deathCases = openCSV_DB(path=pathDeaths,comp=None,enc='latin-1')
    recovCases = openCSV_DB(path=pathRecov,comp=None,enc='latin-1')
    return cases,deathCases,recovCases

if 0:
    datosAbiertosCovid19Mexico='http://187.191.75.115/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip'
    srcDir='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    dMexico = openCSV_DB(path=datosAbiertosCovid19Mexico,comp='zip',enc='latin-1')
    cases, deathCases,recovCases = getCSSEGISandData(urlData=1)

def getTestData():
    urlTests='https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/'
    testsF='covid-testing-all-observations.csv'
    tests = pd.read_csv(urlTests+testsF,index_col=None)
    return test
    #world population Data

def getTestData():
    urlWorldPop='https://stats.oecd.org/sdmx-json/data/DP_LIVE/.POP.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en'
    worldPops = pd.read_csv(urlWorldPop,index_col=None)
    return worlPops

def findFirstCaseDates(a):
    fIndex = list()
    for m in range(len(a)):
        i =  np.where(a[m]>0)[0]
        if len(i)>0:
            ii =i.min()
        else:
            ii = len(a[m])-1
        fIndex.append(ii)
    return np.array(fIndex)

def getIndsSingleRegion(countries, region):
    i = [np.where(countries==region[nn])[0][0] for nn in range(len(region))]
    return i

def getIndsRegions(countries, regions):
    ii =list()
    for mm in range(len(regions)):
        reg = regions[mm]
        ii.append(getIndsSingleRegion(countries,reg))
    return ii
#
def sortDataByCountry(df,nHeaderCols=4):
    """
    Sort data from the same country
    Output:
    x --> Sorted data
    places --> countries sorted as in x
    """
    iCoun= df.iloc[:,1].to_numpy().argsort()
    x = df.iloc[iCoun,nHeaderCols:].to_numpy()
    places = df.iloc[iCoun,1].to_numpy()
    return x, places

def gatherDataSingleCountry(df,country, nHeaderCols=4):
    """
    Gather data from the same country
    """
    cc = df.iloc[:,1].to_numpy()
    countries = np.unique(df.iloc[:,1].to_numpy())
    nCountries = len(countries);
    x = list()
    iC= np.where(cc== country)[0]
    a =df.iloc[iC,nHeaderCols:].to_numpy()
    a.sum(1)
    return a, iC


def gatherDataByCountry(df,nHeaderCols=4):
    """
    Gather data from the same country
    """
    cc = df.iloc[:,1].to_numpy()
    countries = np.unique(df.iloc[:,1].to_numpy())
    nCountries = len(countries);
    x = list()
    for n in range(nCountries):
        iC= np.where(cc== countries[n])[0]
        a =df.iloc[iC,nHeaderCols:].to_numpy()
        x.append(a.sum(0))
    return np.array(x).transpose()

def findCaseStarts(places,cases):
    """
    Find the indices of at which the first cases are observed in each location from the list places.
    """
    startInds = list()
    for n in range(len(places)):
        ii= np.where(cases[n]>0)[0]
        if len(ii)>0:
              startInds.append(ii.min())
        else:
              startInds.append(len(cases[n])-1)
    return np.array(startInds)

# -------------------
# Ratios by array. Correction in cases there are zeros in the denominators
# -------------------
def findHDistance(t,x,y,m,M,nPts=100):
    if (len(t)!=len(x)) | (len(x)!=len(y) ):
        return
    v = np.linspace(m,M,nPts)
    d=list()
    for n in range(len(v)):
        a = np.where(x>v[n])[0][0]
        b = np.where(y>v[n])[0][0]
        d.append(b-a)
    return np.array(d)

def findMode(x):
    xbins = np.unique(x)
    counts,bins =np.histogram(x,xbins)
    return x[counts.argmax()]


def sigmoid(a, aMax=0.1,a0=60.0,n=2):
    aa = a**n
    return aMax* aa /(aa + a0**n)

def correctedArrayRatio(a,b):
    """
    correctedArrayRatio(a,b) calculates a/b from arrays a and b,
    assuming that a is less than or equal to b,
    and correcting for possible zeros in b.
    In those cases, the value of b is set to 1, and the quotient is still 0
    """
    bCorr= b.copy()
    bCorr[bCorr==0]=1
    return np.float64(a)/np.maximum(b,bCorr)

def add_subplot_axes(ax,rect):
    fig = gr.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height])
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax
