def body(data, open='open', close='close'):
	body = abs(data[open] - data[close])
	return data
	
def bullish(data, open='open', close='close'):
	data['bullish'] = data[open] < data[close] 
	return data
	
def bearish(data, open='open', close='close'):
	data['bearish'] = data[open] > data[close]
	return data
