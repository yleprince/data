from requests import get
import json
from datetime import datetime
from os import mkdir, path, system
from time import sleep
from git import Repo

today = datetime.today().strftime("%m-%d-%Y")

PATH = f"./{today}/"  ## HERE : Only line to change
PATH_TO_DOT_GIT = '../..'
commit_message = 'auto update data'

def git_push():
    print('Add, commit and push')
    try:
        repo = Repo(PATH_TO_DOT_GIT)
        repo.git.add(update=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        print('code pushed')
    except:
        print('Some error occured while pushing the code')

def store(urlFunction, suffix, iso):
    filepath = f"{PATH}{iso}_{suffix}.json"
    if path.isfile(filepath):
        print(f"{filepath} already exists")
    else:
        sleep(1)
        r = get(url=urlFunction(iso))
        data = r.json()

        with open(filepath, "w") as outfile:
            json.dump(data, outfile)
        print(f"{filepath} saved")


iso_codes = [
    "AF",
    "AL",
    "DZ",
    "AO",
    "AR",
    "AM",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BD",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BT",
    "BO",
    "BA",
    "BW",
    "BR",
    "BN",
    "BG",
    "BF",
    "BI",
    "KH",
    "CM",
    "CA",
    "CI",
    "CF",
    "TD",
    "DK",
    "DP",
    "DJ",
    "DO",
    "CD",
    "EC",
    "EG",
    "SV",
    "GQ",
    "ER",
    "EE",
    "ET",
    "FK",
    "FJ",
    "FI",
    "FR",
    "GF",
    "TF",
    "GA",
    "GM",
    "GE",
    "DE",
    "GH",
    "GR",
    "GL",
    "GT",
    "GN",
    "GW",
    "GY",
    "HT",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IE",
    "IL",
    "IT",
    "JM",
    "JP",
    "JO",
    "KZ",
    "KE",
    "KP",
    "XK",
    "KW",
    "KG",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LT",
    "LU",
    "MK",
    "MG",
    "MW",
    "MY",
    "ML",
    "MR",
    "MX",
    "MD",
    "MN",
    "ME",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NP",
    "NL",
    "NC",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NO",
    "OM",
    "PK",
    "PS",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PL",
    "PT",
    "PR",
    "QA",
    "RO",
    "RU",
    "RW",
    "SA",
    "SN",
    "RS",
    "SL",
    "SG",
    "SK",
    "SI",
    "SB",
    "SO",
    "ZA",
    "KR",
    "SS",
    "ES",
    "LK",
    "SD",
    "SR",
    "SJ",
    "SZ",
    "SE",
    "CH",
    "SY",
    "TW",
    "TJ",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TT",
    "TN",
    "TR",
    "TM",
    "AE",
    "UG",
    "GB",
    "UA",
    "US",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "EH",
    "YE",
    "ZM",
    "ZW",
]

# ------------------------------------------------------------
## Worldwide

if not path.exists(PATH):
    print(f'creating directory {today}')
    mkdir(PATH)

API = "https://api.thevirustracker.com/free-api?"
timeline = lambda iso: (f"{API}countryTimeline={iso}")
total = lambda iso: (f"{API}countryTotal={iso}")

URL = f"{API}global=stats"

r = get(url=URL)
data = r.json()

with open(f"{PATH}worldwide.json", "w") as outfile:
    json.dump(data, outfile)

## Timelines
for i, iso in enumerate(iso_codes):
    store(timeline, "timeline", iso)

## Countries total
for i, iso in enumerate(iso_codes):
    store(total, "total", iso)

## Meta data
meta = {"export_date": datetime.today().strftime("%m-%d-%Y %H:%M")}
with open(f"{PATH}metadata.json", "w") as outfile:
    json.dump(meta, outfile)

system(f'git add {today}')
system('rm -rf latest')
system(f'cp -r {today} ./latest')
git_push()