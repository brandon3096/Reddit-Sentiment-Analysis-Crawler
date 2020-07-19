class tables:
	schemas = {
		'comment_sentiments': ["(ticker,source,sentiment,received)", "(%s, %s, %s, %s)"]
		, 'word_sentiments': ["(word,sentiment)", "(%s, %s)"]
	}