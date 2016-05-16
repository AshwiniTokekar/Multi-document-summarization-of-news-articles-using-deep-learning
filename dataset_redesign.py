#!/usr/bin/python3
import json
import sys
import dataclean as clean
def main():
	reader = open(sys.argv[1])
	writer = open(sys.argv[2],"w")
	data = reader.readlines()
	for d in data :
		article = json.loads(d)
		text= article["text"]
		lines=text.replace('\n',"#")
		text=''.join(lines)
		text=clean.dataclean(text)
		writer.write(text+"\n")
	writer.close()
	reader.close()

main()		

