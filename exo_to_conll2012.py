

import json
from os import listdir
from os.path import isfile, join


output_file = open("./EXO/srl_conll/exo_srl.txt","w",encoding="utf-8")

dirPath = "./EXO/srl_v3/"
onlyfiles = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]

#print(onlyfiles)


for file in onlyfiles:
	filePath = dirPath+file
	#print(filePath)
	input_file = open(filePath,"r",encoding="utf-8")

	json_data = json.loads(input_file.read())
	#print(json_data)
	for sentence in json_data["sentence"]:
		#print(sentence["text"])
		for srl in sentence["SRL"]:

			output_line = ""+str(srl["word_id"]+1)+" "
			tag = list()

			for word in sentence["word"]:
				output_line += word["text"]+" "
				tag.append("O")
			output_line += "||| "

			for argument in srl["argument"]:
				tag[argument["word_id"]] = "B-"+argument["type"]

			tag[srl["word_id"]] = "B-V"

			for temp in tag:
				output_line += temp + " "

			output_line = output_line.strip() + "\n"
			output_file.write(output_line)

	input_file.close()

dirPath = "./EXO/srl_v4/"
onlyfiles = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
for file in onlyfiles:
	filePath = dirPath+file
	#print(filePath)
	input_file = open(filePath,"r",encoding="utf-8")

	json_data = json.loads(input_file.read())
	#print(json_data)
	for sentence in json_data["sentence"]:
		#print(sentence["text"])
		for srl in sentence["SRL"]:

			output_line = ""+str(srl["word_id"]+1)+" "
			tag = list()

			for word in sentence["word"]:
				output_line += word["text"]+" "
				tag.append("O")
			output_line += "||| "

			for argument in srl["argument"]:
				tag[argument["word_id"]] = "B-"+argument["type"]

			tag[srl["word_id"]] = "B-V"

			for temp in tag:
				output_line += temp + " "

			output_line = output_line.strip() + "\n"
			output_file.write(output_line)

	input_file.close()

output_file.close()