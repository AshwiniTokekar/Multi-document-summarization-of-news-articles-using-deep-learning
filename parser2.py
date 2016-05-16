#!/usr/bin/python3
import json
from json import JSONEncoder
import dataclean as clean
import unicodedata
#This module reads data and converts it to json objects and writes in a file
def dataextraction():
	writer=open("./final_data_sentence.json","w")
	reader= open("./thehindu.json","r")
	data = json.load(reader)
	titles = set()
	i=0
	for d in data:
		if len(d["text"])>0 :
			title = d["title"][0]
			title = unicodedata.normalize('NFKD', title.strip()).encode('ascii','ignore').split("-")[0]
			title = clean.dataclean(title)
			
			if title not in titles : 
				i = i+1
				print title
				titles.add(title)
				texts =""
				headings = ""
				keywords = ""
				if len(d["text"]) > 0:		
					for text in d["text"]:
						texts= texts+clean.dataclean(unicodedata.normalize('NFKD', text).encode('ascii','ignore'))+" "
				if len(d["heading"])>0:
					for heading in d["heading"]:
						headings= heading + clean.dataclean(unicodedata.normalize('NFKD', heading).encode('ascii','ignore'))+","
				if len(d["keywords"])>0:	
					for keywords in d["keywords"]:
						keywords = keywords+ clean.dataclean(unicodedata.normalize('NFKD', keywords).encode('ascii','ignore'))+","
				jstring=JSONEncoder().encode({"id":i+1,"title": title, "text": texts, "keywords" : keywords, "heading" : headings})
				writer.write(jstring+"\n")			
	reader.close()
	writer.close()

def main():
	dataextraction()
main()
