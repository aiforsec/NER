import spotlight
import os
import sys
import requests
import argparse
import pprint as pp
import json
from lxml import html

import urllib.request

import re

from SPARQLWrapper import SPARQLWrapper

from IPython.core.display import JSON

'''
USAGE: python generate_url.py --infile [input text file] --conf [float 0 to 1] --out [prefix of output file]

- conf: number from 0 to 1 for confidence in named entity meaning

ex) python3 generate_url.py --infile reports/test_report.txt --conf 0.5 --out out

'''

URL = "https://api.dbpedia-spotlight.org/en/candidates?"
HEADERS = {"Accept": "application/json"}

HTTP_REX = "http:\/\/\d*"

# TEST_URL = "https://api.dbpedia-spotlight.org/en/candidates?text=This%20report%20investigates%20a%20campaign%20of%20targeted%20malware%20attacks%20that%20has%20successfully%20compromised%201465%20computers%20in%2061%20different%20countries."

# x = requests.get(TEST_URL, headers=headers)
# print(x)
# print(type(x))
# print(x.json())


def main(config):
    if config.infile:
        with open(config.infile, 'r', encoding='utf-8') as file:
            txt = ' '.join(file.read().splitlines())
            num_words = len(txt.split())
            txt = txt.replace(' ', '%20')
    else:
        txt = "Russia%20and%20other%20countries%20in%20the%20Commonwealth%20of%20Independent%20States%20are%20also%20being%20targeted%20and%20compromised."
        num_words = len(txt)

    # print(num_words)

    url = URL + "text={}&confidence={}".format(txt, str(config.conf))
    data = requests.get(url, headers=HEADERS).json()
    for i in range(len(data['annotation']['surfaceForm'])):
        # print(data['annotation']['surfaceForm'][i]['@name'])
        print(data['annotation']['surfaceForm'][i]["resource"]['@uri'])
    print("\ntotal of",len(data['annotation']['surfaceForm']), "names")
    data = json.dumps(data, indent=4)

    # pp.pprint(data)
    with open(config.out + '.json', 'w') as outfile:
        outfile.write(data)


def query(q, epr, f='application/json'):
    try:
        params = {'query': q}
        resp = requests.get(epr, params=params, headers={'Accept': f})
        return resp.text
    except Exception as e:
        print(e, file=sys.stdout)
        raise

# print(num_words)
def disambiguation(name, sparql):
  query = "SELECT DISTINCT ?syn WHERE { { ?disPage dbpedia-owl:wikiPageDisambiguates <http://dbpedia.org/resource/"+name+"> . ?disPage dbpedia-owl:wikiPageDisambiguates ?syn . }  UNION {<http://dbpedia.org/resource/"+name+"> dbpedia-owl:wikiPageDisambiguates ?syn . } }"
  sparql.setQuery(query)
  sparql.setReturnFormat(JSON)
  results_list = sparql.query().convert()
  return results_list

def get_query(name):
    return " SELECT ?uri ?id \
    WHERE {\
     ?uri <http://dbpedia.org/ontology/wikiPageID> ?id.\
     FILTER (?uri = <http://dbpedia.org/resource/"+name+">)}"

def get_uri(temp_string):
    res = re.search(HTTP_REX, temp_string)
    temp = temp_string[res.regs[0][0]:].split("\"")
    return temp[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--infile', type=str, help='report filename')
    parser.add_argument('--out', type=str, help='name of output json', default='out')
    parser.add_argument('--conf', type=float, help='confidence number (0-1)', default=0.5)
    # parser.add_argument('--types', type=str, help='comma-separated list of types for filtering')

    config = parser.parse_args()
    config.conf = 0.9
    config.infile = "raw_text/2015_2015.09.08.musical-chairs-multi-year-campaign-involving-new-variant-of-gh0st-malware_PaloAlto.musical-chairs-multi-year-campaign-involving-new-variant-of-gh0st-malware.pdf.txt"
    # config.infile = "raw_text/2017_2017.07.24.Tick_group_unit42-tick-group-continues-attacks.pdf.txt" # error 1
    # config.infile = "raw_text/2017_2017.07.27.chessmaster-cyber-espionage-campaign_chessmaster-cyber-espionage-campaign.pdf.txt" # same error
    # main(config)

    name = "Palo_Alto_Networks"




    q= "select distinct ?syn where {\
  ?syn (dbpedia-owl:wikiPageDisambiguates|^dbpedia-owl:wikiPageDisambiguates)* dbpedia:name\}"
    p = get_query(name)
    temp_q = query(p, "http://dbpedia.org/sparql")
    # print(temp_q.split("\"type\"\: \"uri\"\, \"value\"\: \""))

    html = get_uri(temp_q)

    r = requests.get(html)
    c = r.content
    print(c)
    outfile = open("out2.txt", "wb")
    outfile.write(c)
    outfile.close()