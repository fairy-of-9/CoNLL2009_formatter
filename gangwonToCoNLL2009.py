import json
import sys
import os



def len_AP(f):  #for conll 2009 format
	buf = []
	pos = []
	result = [0]*200

	for line in f.readlines():
		l = line.strip()
		if l == "":

			max_v = -1
			for x in buf:
				for i in range(len(x[14:])):
					if x[14+i] != '_':
						try:
							result[abs(int(x[0]) - pos[i])] += 1
						except:
							print(x)

			pos = []
			buf = []
			continue
		x = l.split("\t")
		if len(x) <= 1:
			continue

		id, t1, t2, t3, t4, t5, t6, t7, head, t8, t9 = x[:11]

		if x[12] == 'Y':
			pos.append(int(id))

		buf.append(x)  #root = -1
	return


def path_recur(buf, i):

	cur = buf[i]
	result = 0


	while cur != -1:
		result += 1

		if cur == buf[cur]:
			return result

		cur = buf[cur]
	return result


def len_path(f):  #for conll 2009 format
	buf = []
	result = [0]*100

	for line in f.readlines():
		l = line.strip()
		if l == "":

			max_v = -1
			for i in range(len(buf)):
				cur = path_recur(buf,i)
				if cur > max_v:
					max_v = cur

			#result[int((max_v-1)/10)] += 1

			if max_v <= 5:
				result[0]+=1
			elif max_v <= 10:
				result[1]+=1
			elif max_v <= 15:
				result[2]+=1
			elif max_v <= 20:
				result[3]+=1
			else:
				result[4] +=1

			print (max_v, result)


			#buf에 쌓아둔거 일처리.
			buf = []
			continue
		x = l.split("\t")
		if len(x) == 1:
			continue

		id, t1, t2, t3, t4, t5, t6, t7, head, t8, t9 = x[:11]

		buf.append(int(head) - 1)  #root = -1

	return


def cnt_pred(f):  #for conll 2009 format
	result = [0]*25
	cnt = 0

	for line in f.readlines():
		l = line.strip()
		if l == "":
			if cnt == 12:
				print(temp)

			result[cnt] += 1
			print(result)
			cnt = 0
			continue
		x = l.split("\t")
		if len(x) <= 1:
			continue

		temp = l
		if x[12] == 'Y':
			cnt+=1

	return

def cnt_argument(f):  #for conll 2009 format
	result = {}
	cnt = 0

	for line in f.readlines():
		l = line.strip()
		if l == "":
			continue
		x = l.split("\t")
		if len(x) <= 1:
			continue

		temp = l
		args = x[14:]

		for arg in args:
			if arg in result:
				result[arg] += 1
			else:
				result[arg] = 1

	print(result)

	return



def restore_word(w1, w2, feat):
	w = []
	w.append(w1.split("/")[0])
	if feat != "_":
		w.append(feat.split("/")[0])
	if w2 != "_":
		w.append(w2.split("/")[0])
	return "|".join(w)


def parse_conll(f):
	result = []
	buf = []
	tokens = []
	tidx = 0
	err_flag = False
	for line in f.readlines():
		l = line.strip()
		if l == "":
			if not err_flag:
				result.append(buf)
			err_flag = False
			buf = []
			tidx = 0
			continue
		x = l.split("\t")
		if len(x) == 1:
			buf.append(l)
			# print(l)
			tokens = l.split(" ")[1:]
			continue
		try:
			token = tokens[tidx]
			try:
				a = int(token)
				tidx += 1
				token += tokens[tidx]
			except:
				pass
			tidx += 1
			id, w1, w2, pos1, pos2, feat, featpos, feataddpos, head, deprel, pred = x[:11]
			args = x[11:]
			w = restore_word(w1, w2, feat)
			buf.append("\t".join([id, token, w, w, feataddpos, feataddpos, feat, feat, head, head, deprel, deprel, "Y" if pred != "_" else "_", pred] + args))
			# print(buf[-1])
		except:
			err_flag = True
			continue
	return result


def wordCnt_inSentence(f):
	result = []
	buf = []
	tokens = []
	tidx = 0

	cnt = [0]*70
	max_id = -1

	err_flag = False
	for line in f.readlines():
		if line[0] == ';':
			if max_id > 69:
				print(line)
			#print(max_id)
			cnt[max_id] += 1
			max_id = -1

		l = line.strip()
		if l == "":
			if not err_flag:
				result.append(buf)
			err_flag = False
			buf = []
			tidx = 0
			continue
		x = l.split("\t")
		if len(x) == 1:
			buf.append(l)
			# print(l)
			tokens = l.split(" ")[1:]
			continue
		try:
			token = tokens[tidx]
			try:
				a = int(token)
				tidx += 1
				token += tokens[tidx]
			except:
				pass
			tidx += 1
			id, w1, w2, pos1, pos2, feat, featpos, feataddpos, head, deprel, pred = x[:11]


			max_id = int(id) if int(id) > max_id else max_id

			args = x[11:]
			w = restore_word(w1, w2, feat)
			buf.append("\t".join([id, token, w, w, feataddpos, feataddpos, feat, feat, head, head, deprel, deprel, "Y" if pred != "_" else "_", pred] + args))

		except:
			err_flag = True
			continue

	return


def remove_line(f):
	result = []
	for line in f.readlines():
		if line[0] == ';': continue
		result.append(line)

	return result

def sentence_count(f):
	cnt = 0

	for line in f.readlines():
		if line[0] == ';': cnt+=1

	print("cnt :",cnt)

	return

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def word_count(f):
	cnt = 0

	for line in f.readlines():
		if isNumber(line[0]): cnt+=1

	print("cnt :",cnt)

	return

if __name__ == '__main__':
	a = "input_file_path"
	aout = "output_file_path"
	aout2 = "output_file_path"


	with open(a, encoding="EUC-KR") as f:
		r = parse_conll(f)

	with open(aout, "w", encoding="UTF8") as f:
		for line in r:
			f.write("\n".join(line)+"\n\n")


	with open(aout, encoding="UTF8") as f:
		r = remove_line(f)
	with open(aout2, "w", encoding="UTF8") as f:
		for line in r:
			f.write(line)