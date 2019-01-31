import os
import random
from var_dev import product, env
import api_request as API

"""
main function :
    random_category():
        Use to random category of one types
    download_one_page():
        get all items in one page
        download all items

"""


def random_category(__type):
    __categories = product.categories.get(__type, None)
    assert __categories != None
    __leng_cate = len(__categories)
    random_number = random.randrange(0, __leng_cate)
    return __categories[random_number]


def download_one_page(__type, __category):
    _download_dir = env.downloaded_dir.get(__type, None)
    assert _download_dir != None

    _path_dir_to_cate = "{0}{1}".format(_download_dir, __category)
    _path_to_dock_file = "{0}/page/lastest.txt".format(_path_dir_to_cate)
    # get page to download
    if not os.path.exists(_path_to_dock_file):
        # download with page is one
        print(1)
        API.download_a_page(__type, __category)
        return

    API.download_a_page(__type, __category, mode = "continue")
       


def get_page_and_url(__str):
    _ = __str.split("__")
    __page = int(_[0])
    __url = _[1]
    return __page, __url

