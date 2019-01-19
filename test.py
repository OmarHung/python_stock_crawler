import requests

url = "https://www.indiegogo.com/projects/viviva-colorsheets-the-most-portable-watercolors-painting-travel--4#/"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

re =  requests.get(url, headers=headers)
re.encoding = 'utf8'
print(re.text)