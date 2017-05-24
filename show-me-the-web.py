import urllib.request
import os
from urllib.parse import urlparse
from pyquery import PyQuery as pq


def downloadFromUrl(url, root=''):
  path = urlparse(url).path
  file_dir = path.rsplit('/', 1)[0];


  if file_dir != '' and file_dir[0] == '/':
    file_dir = file_dir[1:]

  file_name = path.rsplit('/', 1)[1];
  if '.' not in file_name:
    file_name += '.file'

  if (not os.path.exists(file_dir)) and (file_dir != ''):
    os.makedirs(file_dir)

  file_fullpath = ('' if file_dir == '' else file_dir+'/') + file_name;
  print('-----------------')
  print('Download: '+file_fullpath)
  if not os.path.isfile(file_fullpath):
    urllib.request.urlretrieve(('' if root == '' else root+'/') + url, file_fullpath)
  print('Done!=========')
  print('')
  return file_fullpath

# End function


url = "https://tricia.jp/"
doc_text = urllib.request.urlopen(url).read()
doc = pq(doc_text)
asset_rules = [
  {
    'selector':'link[rel=stylesheet]',
    'attr': 'href',
  },
  {
    'selector':'img[src]',
    'attr': 'src',
  },
  {
    'selector':'script[src]',
    'attr': 'src',
  }
]
# Get the css
for rule in asset_rules:
  for el in doc.items(rule['selector']):
    uri = el.attr[rule['attr']]
    if uri=='':
      break
    if uri[0:2] == '//':
      uri = 'https:' + uri

    if (uri[0:4] != 'http'):
      el.attr[rule['attr']] = downloadFromUrl(uri, root=url)
    else:
      el.attr[rule['attr']] = downloadFromUrl(uri)

outputhtml = "<!DOCTYPE html> <html>"+doc.html(method='html')+"</html>"

text_file = open("index.html", "wt",encoding='utf8')
text_file.write(outputhtml)
text_file.close()


