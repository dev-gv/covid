import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import re

cols=['country','total_cases','new_cases','total_death','new_deaths','recovered',"SKIP",'active_cases','critical','total_cases/10Lakhs','total_death/10lakhs','total_tests','total_test/10lakhs','population']
data = pd.DataFrame(columns=cols)
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url= 'https://www.worldometers.info/coronavirus/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)

    html = urlopen(req,context=ctx).read()
    soup = BeautifulSoup(html)
except:
    print("Turn Your Internet Connection On")
#create a Data frame