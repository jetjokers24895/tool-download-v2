import io
import os
import re
import zipfile
from datetime import datetime

import requests
from lxml.html import document_fromstring

from var_dev import env, product


def write_to_html(text):
    with open("html.txt", "w", encoding="utf-8") as w:
        w.write(text)


def read_html_file():
    with open("html.txt", "r") as r:
        _html = r.read()
    return _html


def send_request(url):
    r = requests.get(url)
    assert r.status_code == 200
    return r.text


def get_items_one_page(number_page, __type, __cate):
    _url = product.base_url_cate.format(number_page, __type, __cate)
    print(_url)
    _html = send_request(_url)
    items = get_urls_img(_html)
    return sorted_items(items)


def sorted_items(__items):
    return sorted(__items, key=lambda x: list(x.keys())[0])


def filter_premium(_divs):
    return [item for item in _divs if item.get("data-multi") != "premium"]


def get_urls_img(html):
    doc = document_fromstring(html)
    _divs = doc.find_class("showcase__item")
    assert len(_divs) > 0
    _divs = filter_premium(_divs)
    _rs = list(map(lambda x: get_data_name_and_id(x), _divs))
    return _rs


def get_data_name_and_id(__item):
    __url_img = __item.get("data-image")
    _name = get_name_of_item(__url_img)
    _id = __item.get("data-id")
    return {_name: _id}


def get_name_of_item(str_input):
    return str_input.split("/")[-1].split("_")[0]


def write_downloaded_line(__type, __category, __page, __url):
    _path_dir = env.downloaded_dir.get(__type, None)
    assert _path_dir != None
    _path_to_page_folder = "{0}{1}/page".format(_path_dir, __category)
    if not os.path.exists(_path_to_page_folder):
        os.makedirs(_path_to_page_folder)

    _path_file = "{0}/{1}.txt".format(_path_to_page_folder, __page)
    print(_path_file)
    with open(_path_file, "a+") as w:
        w.write(__url + '\n')

# get_items_one_page(1, "vector", "animals")


def write_downloaded_line_dock(__page, __category, __type, __url):
    _text = "{0}__{1}".format(__page, __url)

    _download_dir = env.downloaded_dir.get(__type, None)
    assert _download_dir != None

    _path_dir_to_cate = "{0}{1}".format(_download_dir, __category)

    assert _path_dir_to_cate != None

    _path_dir = "{0}/page/lastest.txt".format(_path_dir_to_cate)
    with open(_path_dir, "w") as w:
        w.write(_text)


# write_downloaded_line_dock(1, "animals", "vector", "abc")


def download_a_url(__item_data_download, __type, __category, __page):
    _ = list(__item_data_download.items())
    __item_id = _[0][1]
    __item_name = _[0][0]
    url_to_download = env.base_url_download.format(__item_id)
    # download_file
    download_file(url_to_download, __type, __category, __item_name)
    write_downloaded_line(__type, __category, __page, url_to_download)
    write_downloaded_line_dock(__page, __category, __type, url_to_download)


def change_proxy():
    r = requests.get("http://pubproxy.com/api/proxy?https=true")
    try:
        _data_json = r.json()['data'][0]
        _ip_port = _data_json['ipPort']
        _proxy = "https://{0}".format(_ip_port)
        proxy_dict = {
            'https': _proxy
        }
        return proxy_dict
    except Exception as e:
        print("######Exception###### change_proxy")
        print("Khong the change proxy")
        print(e)
        return None


def download_file(url, __type, __category, folder_name):
    category_path = "{0}{1}/{2}".format(env.download_dir, __type, __category)
    if not os.path.exists(category_path):
        os.makedirs(category_path)

    proxies = change_proxy()
    print(proxies)
    # assert proxies != None
    # print('b')
    with requests.get(url, proxies = proxies, stream=True) as r:
        assert r.status_code == 200
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(
            './download/{0}/{1}/{2}'.format(__type, __category, folder_name))


# def download_file(url, __type, __category, folder_name):
#     category_path = "{0}{1}/{2}".format(env.download_dir, __type, __category)
#     if not os.path.exists(category_path):
#         os.makedirs(category_path)
#     # assert proxies != None
#     # print('b')
#     with requests.get(url, stream=True) as r:
#         assert r.status_code == 200
#         z = zipfile.ZipFile(io.BytesIO(r.content))
#         z.extractall(
#             './download/{0}/{1}/{2}'.format(__type, __category, folder_name))


def get_info_downloaded(__type, __category, __property):
    
    _download_dir = env.downloaded_dir.get(__type, None)
    assert _download_dir != None

    _path_dir_to_cate = "{0}{1}".format(_download_dir, __category)

    if not os.path.exists(_path_dir_to_cate):
        print(f"Category :{__category} havent downloaded yet")
        return None

    _path_to_open = "{0}/page/lastest.txt".format(_path_dir_to_cate)
    try:
        with open(_path_to_open, 'r') as f:
            __str = f.read()
            __page, __url = get_page_and_url(__str)
            return {"page": __page, "url": __url}.get(__property, None)

    except Exception as e:
        # if file doesnt exist, create file -> write 0 -> return 0
        print(_path_to_open + " khong ton tai")
        print(e)
        print("#######Creating#######")
        with open(_path_to_open, "w") as w:
            w.write("1")
        return 1

def get_page_and_url(__str):
    _ = __str.split("__")
    __page = int(_[0])
    __url = _[1]
    return __page, __url

def find_a_item(__url, last_working_page, __type, __category):
    _page = last_working_page

    _page_downloaded = get_info_downloaded(__type, __category, "page")
    assert _page_downloaded != None

    # If the item is deleted, tool will download  next page
    if _page - _page_downloaded == 4:
        return []

    _items = get_items_one_page(last_working_page, __type, __category)
    if find_index_of_item(_items, __url) is None:
        find_a_item(__url, _page + 1, __type, __category)  # de quy

    return _items


def find_index_of_item(__items, __url):
    __id = get_id_from_url(__url)
    for i in range(0,len(__items)):
        if list(__items[i].values())[0] == __id:
            return i
    return None


def get_id_from_url(__url):
    __rs = re.findall(r'\d', __url)
    return ''.join(__rs)

def get_download_dock(__type, __category):
    __page_downloaded = get_info_downloaded(__type, __category,"page")
    __url = get_info_downloaded(__type, __category, "url")

    assert __page_downloaded != None and __url != None
    __items = get_items_one_page(__page_downloaded, __type, __category)

    try:
        _index = find_index_of_item(__items, __url)
        if _index == len(__items) - 1:
            return [],__page_downloaded
        if not _index is None:
            __items = __items[_index + 1:]
        else:
            __items = get_download_dock_in_exception_case(
                                        __url, __page_downloaded, __type, __category)
    except ValueError as e:
        print("#########EXCEPTION#### get_download_dock")
        print(e)

    return __items, __page_downloaded


def get_download_dock_in_exception_case(__url, last_working_page, __type, __category):
    __items = find_a_item(__url, last_working_page, __type, __category)
    if __items == []:
        return []
    try:
        _index = find_index_of_item(__items, __url)
        if _index == len(__items) - 1:
            return []
        return __items[_index + 1:] if not _index is None else __items
    except Exception as e:
        print("#############EXCEPTION###### get_download_dock_in_exception_case")
        print(e)
        return __items


def download_a_page(__type, __category, mode= "new"):
    if mode == "new":
        __page = 1
        __data = get_items_one_page(__page, __type, __category)
        for i in __data:
            download_a_url(i, __type, __category, __page)
    
    if mode == "continue":
        __items_downloading, _page_downloaded = get_download_dock(__type, __category)
        if __items_downloading != []:
            for __item in __items_downloading:
                download_a_url(__item, __type, __category,                                                         _page_downloaded)
        __page = _page_downloaded + 1
        __data = get_items_one_page(__page, __type, __category)
        for i in __data:
            download_a_url(i, __type, __category, __page)



# try:
#     data = get_items_one_page(1, "vector", "animals",)
#     download_a_url(data[0], "vector", "animals", 1)
# except Exception as e:
#     print(e)
