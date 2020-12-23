import requests
import argparse
import pprint as pp
import json

'''
USAGE: python generate_url.py --infile [input text file] --conf [float 0 to 1] --out [prefix of output file]

- conf: number from 0 to 1 for confidence in named entity meaning

ex) python3 generate_url.py --infile reports/test_report.txt --conf 0.5 --out out

'''

URL = "https://api.dbpedia-spotlight.org/en/candidates?"
HEADERS = {"Accept": "application/json"}

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
		print(data['annotation']['surfaceForm'][i]['@name'])

	data = json.dumps(data, indent=4)

	# pp.pprint(data)
	with open(config.out + '.json', 'w') as outfile:
		outfile.write(data)
	
	# print(num_words)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('--infile', type=str, help='report filename')
	parser.add_argument('--out', type=str, help='name of output json', default='out')
	parser.add_argument('--conf', type=float, help='confidence number (0-1)', default=0.5)
	# parser.add_argument('--types', type=str, help='comma-separated list of types for filtering')

	config = parser.parse_args()
	main(config)