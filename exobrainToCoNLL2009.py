

import json
from os import listdir
from os.path import isfile, join


output_file = open("output_file_path","w",encoding="utf-8")

dirPath = "input_directory_path"
onlyfiles = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
sentence_cnt = 0

cnt = [0] * 200  # 문장내 단어수.

for file in onlyfiles:
	filePath = dirPath+file
	print(filePath)
	input_file = open(filePath,"r",encoding="utf-8")

	json_data = json.loads(input_file.read())
	#print(json_data)



	sentence_cnt += len(json_data["sentence"])
	for sentence in json_data["sentence"]:

		cnt[len(sentence["word"])] += 1
		if len(sentence["word"]) > 70:
			print('!!!')
			print(sentence)

		for word in sentence["word"]:
			id = int(word["id"])
			form = word["text"]
			begin, end = word["begin"], word["end"]

			lemma = []
			pos = []
			for morp in sentence["morp"]:
				if int(morp["id"]) < begin:
					continue
				if int(morp["id"]) > end:
					break
				lemma.append(morp["lemma"])
				pos.append(morp["type"])
			lemma = "|".join(lemma)
			pos = "|".join(pos)

			feat = '_'

			head = 987654321
			deprel = '_'
			for dep in sentence["dependency"]:
				if int(dep["id"]) == id:
					head = int(dep["head"])+1
					deprel = dep["label"]
					break
			if head == 987654321:
				#print ('no head!!')
				head = '_'

			fillpred = '_'
			verb_text = ''
			args = []
			for srl in sentence["SRL"]:
				if int(srl["word_id"]) == id:
					fillpred = 'Y'
					verb_text = srl["verb"]

				for argument in srl["argument"]:
					if int(argument["word_id"]) == id:
						args.append(argument["type"])



			pred = '_'
			if verb_text != '':
				for wsd in sentence["WSD"]:
					if int(wsd["begin"]) < begin:
						continue
					if int(wsd["end"]) > end:
						break

					if verb_text in wsd["text"]:
						pred = verb_text + '.' + wsd["scode"]


			while len(args) < len(sentence["SRL"]):
				args.append('_')



			error_flag = 0
			if fillpred == 'Y' and pred == '_':
				#print('error')
				pred = verb_text + '.' + '01'
				#print('pred : _ -> ' + pred)
				error_flag = 1



			id += 1
			output_line = "\t".join([str(id),form, lemma, lemma, pos, pos, feat, feat, str(head), str(head), deprel, deprel, fillpred, pred] + args)
			output_line += '\n'
			if id == 1:
				output_line = '\n' + output_line

			if error_flag:
				print(output_line)

			output_file.write(output_line)

	input_file.close()

output_file.close()