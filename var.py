import os


class product:

    base_url = "https://www.freepik.com/index.php?goto=8&populares=1&page={0}&type={1}"
    base_url_cate = "https://www.freepik.com/search?query={2}&sort=popular&type={1}&format=search&page={0}"

    categories = {
        'photo': ["Abstract",
                  "Animal",
                  "Architecture",
                  "Baby",
                  "Birthday",
                  "Book",
                  "Business",
                  "Coffee",
                  "Communication",
                  "Community",
                  "Couple",
                  "Dance",
                  "Education",
                  "Family",
                  "Fashion",
                  "Fitness",
                  "Flower",
                  "Food",
                  "Frame",
                  "Friends",
                  "Gifts",
                  "Hand",
                  "Health",
                  "Laptop",
                  "Lifestyle",
                  "Liquid",
                  "Love",
                  "Music",
                  "Nature",
                  "Party",
                  "Pet",
                  "Phone",
                  "Portrait",
                  "Real state",
                  "Sales",
                  "Season",
                  "Shopping",
                  "Sky",
                  "Spa",
                  "Sport",
                  "Table",
                  "Technology",
                  "Texture",
                  "Travel",
                  "Water",
                  "Wedding",
                  "Wood",
                  "Yoga",
                  "Interior"],
        'vector': ["Animals",
                     "Background",
                     "Banners",
                     "Birthday",
                     "Business",
                     "Buttons",
                     "Cartoon",
                     "Christmas",
                     "Design elements",
                     "Easter",
                     "Graphics",
                     "Halloween",
                     "Human",
                     "Icons",
                     "Illustrations",
                     "Logo templates",
                     "Map",
                     "Music",
                     "Nature",
                     "Objects",
                     "Ornament",
                     "Ribbons",
                     "Silhouettes",
                     "Sports",
                     "Summer",
                     "Templates",
                     "Textures",
                     "Transport",
                     "Valentine",
                     "Water",
                     "Web elements",
                     "Web templates",
                     "Wedding",
                     "Signs and symbols",
                     "Travel",
                     "Food",
                     "Country",
                     "Event",
                     "Technology",
                     "Education",
                     "Health",
                     "Calendar"],
        'psd': ["Backgrounds",
                "Buttons",
                "Calendars",
                "Cards",
                "Colours",
                "Effects",
                "Emails",
                "Icons",
                "Illustrations",
                "Logos",
                "Objects",
                "Print templates",
                "Text effects",
                "Textures",
                "Web elements",
                "Web templates",
                "Ui kit",
                "Mockup"]
    }
    type_of_items = [
        # 'iconos',
        'photo'
        'vector'
        'psd'

    ]
    number_page = {
        'photo': 37986,
        'vector': 31151,
        'psd': 113,
    }


class dev:
    url = "https://www.freepik.com/free-psd"


class env:
    WORKING_DIR = os.getcwd()
    test = False
    base_url_download = "https://download.freepik.com/{0}?lang=en"
    logs_path_dir = '{0}/logs/'.format(WORKING_DIR)

    download_dir = '{0}/download/'.format(WORKING_DIR)
    downloaded_file = {
        'photo': '{0}photo/page/'.format(download_dir),
        'vector': '{0}vector/page/'.format(download_dir),
        'psd': '{0}psd/page/'.format(download_dir)
    }

    download_dock = {
        'photo': 'photo/dock_photo.txt',
        'vector': 'vector/dock_vector.txt',
        'psd': 'psd/dock_psd.txt'
    }

    change_network = "{0}/change_ip.exe".format(WORKING_DIR)


class test:
    photo = "https://www.freepik.com/free-photo/golden-silver-christmas-deco-on-black_3239044.htm"
