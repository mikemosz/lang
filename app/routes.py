from flask import render_template
from flask import request
from flask import url_for

import pandas as pd 

from app import app

@app.route('/')
def index():
	df_words = pd.read_csv('data/ny.csv')
	word = df_words.sample().iloc[0].to_dict()

	prompt, answer = word['definition'], word['root']

	if request.args.get('json'):
		json = {'prompt':prompt,'answer':answer}
		print(json)
		return json
	else:
		return render_template('quiz.html', prompt=prompt, answer=answer)