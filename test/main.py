from var_dev import product
import api_download as API


def router(__type):
    return {
        'vector': 'photo',
        'photo': 'psd',
        'psd': 'vector'
    }.get(__type, None)


def download():
    __type__downloading = "vector"
    while 1:
        __category =API.random_category(__type__downloading)
        API.download_one_page(__type__downloading, __category)
        __type__downloading = router(__type__downloading)
        assert __type__downloading != None


if __name__ == "__main__":
    download()

    while 1:
        pass
