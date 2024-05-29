import requests
resp = requests.post('https://textbelt.com/text', {
  'phone': '9821898939',
  'message': 'Hello world',
  'key': 'textbelt',
})
print(resp.json())