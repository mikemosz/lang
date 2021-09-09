from flask import render_template
from flask import request
from flask import url_for

import math
import numpy as np
import pandas as pd 

from app import app

EN_PRON = {
	'nom': {'sg': ['I','you','he'],    'pl': ['we','you (pl.)','they']},
	'acc': {'sg': ['me','you','him'],  'pl': ['us','you (pl.)','them']},
	'gen': {'sg': ['my','your','his'], 'pl': ['our','your (pl.)','their']},
}

EN_NUM = ['one','two','three','four','five']

EN_DEM = {
	'prox':  ('this', 'these'),
	'dist':  ('that', 'those'),
	'rem':   ('that', 'those'),
	'all':   ('the whole', 'all the'),
	'other': ('another','other'),
	'every': ('every',''),
}

NY_CONCORD = {
	'prox': 'uyu awa uwu iyi ili awa ichi izi iyi izi - aka iti uwu'.split(),
	'dist': 'uyo awo uwo iyo ilo awo icho izo iyo izo - ako ito uwo'.split(),
	'pron': 'ye  o   wo  yo  lo  o   cho  zo  yo  zo  - ko  to  wo'.split(),
	'subj': 'a   a   u   i   li  a   chi  zi  i   zi  - ka  ti  u'.split(),
	'obj':  'm   wa  u   yi  li  wa  chi  zi  yi  zi  - ka  ti  u'.split(),
	'num':  'm   a   u   i   li  a   chi  zi  i   zi  - ka  ti  u'.split(),
	'rem':  'u   a   u   i   li  a   chi  zi  i   zi  - ka  tu  u'.split(),
	'poss': 'wa  a   wa  ya  la  a   cha  za  ya  za  - ka  ta  wa'.split(),
	'vadj': 'wo  o   wo  yo  lo  o   cho  zo  yo  zo  - ko  to  wo'.split(),
	'oth':  'wi  e   wi  i   li  e   chi  zi  i   zi  - ke  ti  wi'.split(),
}

NY_PRON = {
	'nom': {'sg': ['ndi','u','a'],   'pl': ['mui','mu','a']},
	'acc': {'sg': ['ndi','ku','mu'], 'pl': ['ti','ku','wa']},
	'gen': {'sg': ['nga','ko','ke'], 'pl': ['thu','nu','wo']},
	'ind': {'sg': ['ne','we','ye'],  'pl': ['fe','nu','wo']},
}

NY_NUM = ['modzi','wiri','tatu','nayi','sanu']

def render_en(word, args):
	base = word['definition']

	if word['part'] == 'n':
		if args['number'] == 'pl':
			if base == 'child':
				return 'children'
			elif base == 'foot':
				return 'feet'
			elif base.endswith('fe'):
				base = base[:-2] + 'ves'
			elif base.endswith('man'):
				base = base[:-3] + 'men'
			elif base.endswith('y') and not base.endswith(('ay','ey','oy')):
				base = base[:-1] + 'ies'
			elif base.endswith(('s','sh','ch','o')):
				base = base + 'es'
			else:
				base = base + 's'

		if 'poss_number' in args:
			return ' '.join((EN_PRON['gen'][args['poss_number']][args['poss_person'] - 1], base))
		elif 'quantity' in args:
			return ' '.join((EN_NUM[args['quantity'] - 1], base))
		elif 'distance' in args:
			num_idx = int(args['number'] == 'pl')
			out = ' '.join((EN_DEM[args['distance']][num_idx], base))
			if args['distance'] == 'dist':
				out += ' there'
			return out
		else:
			return base

def render_ny(word, args):
	base = word['root']
	
	if word['part'] == 'n':
		nclass = int(word[args['number'] + '_class'])
		if args['number'] == 'pl':
			base = word['plural']

		if 'poss_number' in args:
			return ' '.join((base, NY_CONCORD['poss'][nclass - 1] + NY_PRON['gen'][args['poss_number']][args['poss_person'] - 1]))
		elif 'quantity' in args:
			return ' '.join((base, NY_CONCORD['num'][nclass - 1] + NY_NUM[args['quantity'] - 1]))
		elif 'distance' in args:
			if args['distance'] in ('prox','dist'):
				dem = NY_CONCORD[args['distance']][nclass - 1]
			elif args['distance'] == 'other':
				dem = NY_CONCORD['oth'][nclass - 1] + 'na'
			elif args['distance'] == 'rem':
				dem = NY_CONCORD['rem'][nclass - 1] + 'ja'
			elif args['distance'] == 'all':
				dem = NY_CONCORD['pron'][nclass - 1] + 'nse'				
			elif args['distance'] == 'every':
				dem = NY_CONCORD['subj'][nclass - 1] + 'li' + NY_CONCORD['pron'][nclass - 1] + 'nse'

			return ' '.join((base, dem))				
		else:
			return base

@app.route('/')
def index():
	df_words = pd.read_csv('data/ny.csv')
	word = df_words[(df_words.part == 'n')].sample().iloc[0].to_dict()

	if word['part'] == 'n':
		if not isinstance(word['plural'], str):
			args = {'number': 'sg'}
			args['mode'] = np.random.choice(('nom','poss'), p=(0.75, 0.25)) 
		else:
			args = {'number': np.random.choice(('sg','pl'), p=(0.6,0.4))}
			args['mode'] = np.random.choice(('','poss','num','dem'), p=(0.4,0.2,0.2,0.2))
	
		if 'mode' not in args:
			pass
		elif args['mode'] == 'poss':
			args['poss_number'] = np.random.choice(('sg','pl'))
			args['poss_person'] = np.random.choice((1,2,3))
		elif args['mode'] == 'num':
			if args['number'] == 'sg':
				args['quantity'] = 1
			else:
				args['quantity'] = np.random.choice((2,3,4,5))
		elif args['mode'] == 'dem':
			dem_choices = ['prox','dist','rem','all']
			if args['number'] == 'sg':
				dem_choices.append('every')

			args['distance'] = np.random.choice(dem_choices)

	print(word, args)

	prompt, answer = render_en(word, args), render_ny(word, args)

	if request.args.get('json'):
		json = {'prompt':prompt,'answer':answer}
		return json
	else:
		return render_template('quiz.html', prompt=prompt, answer=answer)