import pandas as pd
import requests
import lxml.html as lh
import csv

def get_current_year(data):
    for iter in data['gameAttributes']:
        #print(iter)
        if iter['key'] == 'season':
            return iter['value']

def get_phase(data):
    for iter in data['gameAttributes']:
        if iter['key'] == 'phase':
            return iter['value']
