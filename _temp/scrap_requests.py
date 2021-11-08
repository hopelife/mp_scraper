# [파이썬 XML 다루는 법 (PYTHON XML)](https://dololak.tistory.com/253)


import os, sys
import requests
# import urllib
# from urllib import request

import lxml.html as etree

##------------------------------------------------------------
## User 모듈
##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '.')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from utils_basic import (_read_file, _write_file, _fn)


def request(url='', method='get', headers=None, data=None):
    return requests.get(url, headers=headers)


# def request_get(url='', headers=None, params=None):
def request_get(url, kwargs={}):
    """
    kwargs: {'headers':'', 'params':''}
    """
    return requests.get(url, **kwargs)


def request_post(url='', headers=None, data=None):
    pass


def request_put(url='', headers=None, data=None):
    pass


def request_delete(url='', headers=None, data=None):
    pass


def request_patch(url='', headers=None, params=None):
    pass


def _page_source(url, local=False, method='get', kwargs=None):
    """
    페이지 소스
    type: local / remote
    """
    # recvd.text
    pass


# def _tree_from_file(path, encoding='UTF-8', parser=None):
def _tree_from_file(path, encoding='UTF-8'):
    return etree.fromstring(_read_file(path, encoding=encoding))


def _tree_from_string(source=''):
    return etree.fromstring(source)


# def _text_by_xpath(root, xpath=None, trim=True, all=True, one=True):
def _texts_by_xpath(root, xpath=None):
    node = _node_by_xpath(root, xpath=None)
    ## NOTE: text_content(), '//text()' 차이점
    # return [e.text_content().strip() for e in node.xpath(xpath)]
    return [e.strip() for e in node.xpath(f"{xpath}//text()")]


def _attr_by_xpath(root, xpath=None, attr=None):
    return root.attrib[attr]

def _node_by_xpath(root, xpath=None):
    """
    root 기준 xpath에 해당하는 node
    """
    return root if xpath==None else root.xpath(xpath)


def _root_tree(source='', type='url', method='get'):
    """
    type: file / url / text
    source: path(file), url(url), string(text)
    """
    if type == 'url':
        root_tree = etree.parse(source)  # 'http://www.naver.com'
    elif type == 'file':
        # root_tree = fromstring(_read_file(source))  # 'C:/users.xml'
        root_tree = etree.parse(source)  # 'C:/users.xml'
    elif type == 'text':
        root_tree = etree.fromstring(source)  # '<div>text1</div>'
        # root_tree = elemTree.fromstring(source)

    return root_tree

# find_rel_links(rel):
# from lxml import etree, html
# import urlparse

# def fix_links(content, absolute_prefix):
#     """
#     Rewrite relative links to be absolute links based on certain URL.

#     @param content: HTML snippet as a string
#     """

#     if type(content) == str:
#         content = content.decode("utf-8")

#     parser = etree.HTMLParser()

#     content = content.strip()

#     tree  = html.fragment_fromstring(content, create_parent=True)

#     def join(base, url):
#         """
#         Join relative URL
#         """
#         if not (url.startswith("/") or "://" in url):
#             return urlparse.urljoin(base, url)
#         else:
#             # Already absolute
#             return url

#     for node in tree.xpath('//*[@src]'):
#         url = node.get('src')
#         url = join(absolute_prefix, url)
#         node.set('src', url)
#     for node in tree.xpath('//*[@href]'):
#         href = node.get('href')
#         url = join(absolute_prefix, href)
#         node.set('href', url)

#     data =  etree.tostring(tree, pretty_print=False, encoding="utf-8")

#     return data


# def download(url, file_name):
#     with open(file_name, "wb") as file:   # open in binary mode
#         response = get(url)               # get request
#         file.write(response.content)      # write to file

# rewrite_links
# .rewrite_links(link_repl_func, resolve_base_href=True, base_href=None)

##============================================
## 보조 함수
##============================================
# {
#     r'\n{2,}': '\n',

# }

def prettify_source(source=''):
    pass


if __name__ == '__main__':
    pass
    # NOTE: requests
    kwargs = {
        "headers": {'Content-Type': 'application/json; charset=utf-8'},
        "params": {"userId": "1"}
    }

    r = request_get('https://www.daleseo.com/python-requests/', kwargs)
    print(f"{r.text}")

