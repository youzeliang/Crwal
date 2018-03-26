from urllib import request, error
try:
    response = request.urlopen('http://cuiqingcai.com/iddddndex.htm')
except error.URLError as e:
    print(e.reason)


# tese