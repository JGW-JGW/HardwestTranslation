# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time  : 2023-05-06 21:13
# Author: jgw
from pprint import pprint
from typing import List, Dict, Union
import random as rd
import math
import datetime as dt
import re
from abc import ABCMeta, abstractmethod
import os
import glob
import yaml

"""
读取文件，翻译并放到另一个地方
"""

""" 读取正式文件，并根据yaml文件生成新文件 """

steam_filepath = 'D:\\Steam\\steamapps\\common\\HardWest\\Data\\Texts'
output_filepath = 'D:\\00Software\\Steam\\HardWest\\Texts'

with open('translator.yml', 'r', encoding='utf-8') as f_yml:
	translator = yaml.safe_load(f_yml)

for steam_file in glob.glob(os.path.join(steam_filepath, '*.tsv')):
	base_filename = os.path.basename(steam_file)
	sub_translator = translator[base_filename]
	output_file = os.path.join(output_filepath, base_filename)

	with open(steam_file, 'r', encoding='utf-8') as f_steam:
		with open(output_file, 'w', encoding='utf-8') as f_output:
			first_line = f_steam.readline()

			n_col = len(first_line.split('\t'))

			f_output.write(first_line)

			second_line = f_steam.readline()

			f_output.write(second_line)

			for line in f_steam:
				tmp = line.split('\t')

				if len(tmp) != n_col:
					raise ValueError(
						f'inconsistent length: line = \"{line}\", n_split = {len(tmp)}; n_col = {n_col}'
					)

				item = tmp[0]
				len_chars = tmp[3]

				if item != '' and len_chars != '0':
					if item in sub_translator:
						en = tmp[2]

						if en != sub_translator[item]['en']:
							print(f'[WARNING] INCONSISTENT EN: en = \"{en}\"; filename = {base_filename}, item = {item}')

						tmp[2] = sub_translator[item]['chn']
						tmp[3] = str(len(tmp[2]))
						tmp[4] = str(len(tmp[3].split(' ')))

						f_output.write('\t'.join(tmp))

					else:
						print(f'[WARNING] NOT FOUND EN: en = \"{en}\"; filename = {base_filename}, item = {item}')
						f_output.write(line)

				else:
					f_output.write(line)


""" 搞定 Texts 文件夹内的文件 """

# en_filepath = 'D:\\00Software\\Steam\\Data_原版\\Texts'
# chn_filepath = 'D:\\00Software\\Steam\\Data_汉化版\\Texts'
#
# # 按格式打印，用来快速粘贴到yaml文件里
# for item in glob.glob(os.path.join(en_filepath, '*.tsv')):
# 	base_filename = os.path.basename(item)
# 	print(f'{base_filename}:')
#
# 	chn_filename = os.path.join(chn_filepath, base_filename)
# 	memo = dict()
# 	if os.path.isfile(chn_filename):
# 		with open(chn_filename, 'r', encoding='utf-8') as f:
# 			first_line = f.readline()
#
# 			n_col = len(first_line.split('\t'))
#
# 			f.readline()
#
# 			for line in f:
# 				tmp = line.split('\t')
#
# 				if len(tmp) != n_col:
# 					raise ValueError(
# 						f'inconsistent length: line = \"{line}\", n_split = {len(tmp)}; n_col = {n_col}'
# 					)
#
# 				if tmp[0] != '' and tmp[3] != '0':
# 					memo[tmp[0]] = tmp[2].replace('"', '\\"').replace("'", "\\'")
#
# 	en_filename = os.path.join(en_filepath, base_filename)
# 	with open(en_filename, 'r', encoding='utf-8') as f:
# 		first_line = f.readline()
#
# 		n_col = len(first_line.split('\t'))
#
# 		f.readline()
#
# 		for line in f:
# 			tmp = line.split('\t')
#
# 			if len(tmp) != n_col:
# 				raise ValueError(
# 					f'inconsistent length: line = \"{line}\", n_split = {len(tmp)}; n_col = {n_col}'
# 				)
#
# 			if tmp[0] != '' and tmp[3] != '0':
# 				print(f'  {tmp[0]}:')
# 				en = tmp[2].replace('"', '\\"').replace("'", "\\'")
# 				print(f'    en: \"{en}\"')
# 				chn = memo[tmp[0]] if tmp[0] in memo else 'NULL'
# 				print(f'    chn: \"{chn}\"')
