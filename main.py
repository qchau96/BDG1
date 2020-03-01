import os
import json
import argparse
from sodapy import Socrata

parser = argparse.ArgumentParser(description='python command line interface that can connect to the OPCV API')
parser.add_argument('--page_size', type=int, required=True, default=1000, help='page size')
parser.add_argument('--num_pages', type=int, default=None, help='num pages')
parser.add_argument('--output', type=str, default=None, help='the path for output')

args = parser.parse_args()
page_size = args.page_size
num_pages = args.num_pages
output = args.output

client = Socrata(
	"data.cityofnewyork.us",
	os.getenv('APP_KEY')
)

if output:
	file_writer = open(output, "w")

outputs = []
if num_pages:
	for page_int in range(num_pages):
		rows = client.get("nc67-uf89", offset=page_size*page_int, limit=page_size)
		if output:
			for row in rows:
				file_writer.write(json.dumps(row) + "\n")
		outputs.extend(rows)

else:
	i = 0
	while True:
		rows = client.get("nc67-uf89", offset=page_size*i, limit=page_size)
		outputs.extend(rows)
		if output:
			for row in rows:
				file_writer.write(json.dumps(row) + "\n")
		if not rows:
			break
		i = i + 1
for i in outputs:
	print (i)