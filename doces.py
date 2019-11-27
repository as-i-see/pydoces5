from __future__ import absolute_import, unicode_literals

import pprint

import esprima


def es_file_doc(path='test/tests12/Book666.js'):
  ast_dict = src_ast_dict(path)
  pprint.pprint(ast_dict, compact=True)

def ast_to_html(ast:dict):
  pass

def src_ast_dict(path='test/tests12/Book666.js') -> dict:
  with open(path, 'rU') as f:
    s = f.read()
  sast = esprima.parseScript(s, {'attachComment': True})
  dast = esprima.toDict(sast)
  all_dockblocks_to_dict(dast)
  return dast


def all_dockblocks_to_dict(srcdict: dict):
  for item in srcdict['body']:
    if 'leadingComments' in item.keys():
      if len(item['leadingComments']) == 2:
        srcdict['doc'] = gen_docdict(item['leadingComments'][0]['value'])
        docblock_to_dict(item)


def docblock_to_dict(srcdict: dict):
  leading_comments = srcdict['leadingComments']
  lowest_comment = leading_comments[len(leading_comments) - 1]
  srcdict['doc'] = gen_docdict(lowest_comment['value'])


def gen_docdict(docblock: str) -> dict:
  dictdoc = {}
  for line in docblock.strip().replace("*", "").splitlines():
    line = line.strip()
    if line.startswith("@"):
      tokens = line.split(' ', 1)
      annotation = tokens[0].replace('@', '', 1)
      if len(tokens) > 1:
        if annotation in dictdoc.keys():
          dictdoc[annotation].append(tokens[1])
        else:
          dictdoc[annotation] = [tokens[1]]
      else:
        dictdoc[annotation] = ''
    else:
      tokens = line.split(' ', 1)
      dictdoc['description'] = tokens[1]
  # print('\n')
  pprint.pprint(dictdoc)
  return dictdoc