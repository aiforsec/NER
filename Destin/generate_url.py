import requests
import argparse
import pprint as pp
import json
from SPARQLWrapper import SPARQLWrapper, JSON

'''
USAGE: python generate_url.py --infile [input text file] --conf [float 0 to 1] --out [prefix of output file]

- conf: number from 0 to 1 for confidence in named entity meaning

ex) python3 generate_url.py --infile reports/test_report.txt --conf 0.5 --out out
'''

URL = "https://api.dbpedia-spotlight.org/en/candidates?"
HEADERS = {"Accept": "application/json"}


def get_properties(uri, out_prefix):
	# initialize SPARQL endpoint
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setReturnFormat(JSON)

	# query results
	queryString = """SELECT ?p ?o
		WHERE 
		{{ 
			<http://dbpedia.org/resource/{}> ?p ?o 
			BIND (lang(?o) as ?lang)
			FILTER (?lang = 'en' || !bound(?lang))
		}}""".format(uri)

	sparql.setQuery(queryString)
	results = sparql.query().convert() # dictionary full of triple matches
	result_str = json.dumps(results, indent=4) # string to dump into json file
	# print(results)

	# for match in results["results"]["bindings"]:
	#	if match["p"]["value"].endswith("type"):
	#		print(match["o"]["value"].split('#')[-1])
	
	# with open(out_prefix + '.json', 'w') as outfile:
	#	outfile.write(result_str)

	# print(queryString)

	return results

def main(config):
	# open text file
	if config.infile:
		with open(config.infile, 'r', encoding='utf-8') as file:
			# replace spaces with %20
			txt = ' '.join(file.read().splitlines())
			num_words = len(txt.split())
			txt = txt.replace(' ', '%20')
	else:
		# sample text file if not provided
		txt = "Russia%20and%20other%20countries%20in%20the%20Commonwealth%20of%20Independent%20States%20are%20also%20being%20targeted%20and%20compromised."
	

	# request annotations of text from DBPedia in JSON format
	url = URL + "text={}&confidence={}".format(txt, str(config.conf))
	data = requests.get(url, headers=HEADERS).json()
	data_str = json.dumps(data, indent=4)

	# output candidates
	pp.pprint(data_str)
	with open(config.out + '.json', 'w') as outfile:
		outfile.write(data_str)

	# get properties on DBPedia page for each candidate
	cand_dict = dict()
	for cand in data["annotation"]["surfaceForm"]:
		uri = cand["resource"]["@uri"]
		print(uri)
		cand_res = get_properties(uri, config.out_prop)
		cand_dict[uri] = cand_res["results"]["bindings"]
	
	cand_json = json.dumps(cand_dict, indent=8)
	with open("all_cands.json", "w") as outfile:
		outfile.write(cand_json)



if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	# arguments
	parser.add_argument('--infile', type=str, help='report filename', default='reports/test_report.txt')
	parser.add_argument('--out', type=str, help='name of output json', default='out')
	parser.add_argument('--conf', type=float, help='confidence number (0-1)', default=0.5)
	# parser.add_argument('--types', type=str, help='comma-separated list of types for filtering')

	config = parser.parse_args()
	main(config)