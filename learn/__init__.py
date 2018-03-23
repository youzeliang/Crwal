import urllib.request

response = urllib.request.urlopen('https://www.python.org')
# print(response.read().decode('utf-8')) #type I
print (response.status)
print (response.getheaders())



