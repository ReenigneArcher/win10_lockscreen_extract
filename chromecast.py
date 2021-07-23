import configparser
import logging
import os
import re
import requests
import shutil
import uuid
from PIL import Image

# local imports
import util


def initialize(img_path, logger: logging.Logger):
    logger.info('Initializing directories...')

    if not os.path.isdir(img_path):
        logger.info('{0} does not exists. Creating it...'.format(img_path))
        os.mkdir(img_path)

    if not os.path.isdir(img_path / 'dups/'):
        logger.info('{0} does not exists. Creating it...'
                    .format(img_path / 'dups/'))
        os.mkdir(img_path / 'dups/')


def main(config: configparser.ConfigParser):
    logfile = util.get_conf_logfile(config, default='log')
    loglevel = util.get_conf_loglevel(config, default=logging.DEBUG)

    logger = logging.getLogger(__file__)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:'
                                  '%(lineno)d(%(funcName)s) %(msg)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(loglevel)

    util.check_os(logger=logger)

    logger.info('Downloading new files...')

    img_path = util.get_conf_imgpath(config)
    initialize(img_path, logger=logger)

    url = 'https://clients3.google.com/cast/chromecast/home'
    r = requests.get(url)

    for match in re.finditer(r"(ccp-lh\..+?mv)", r.text, re.S):
        #print('------')
        #print(match.group(1))
        image_link = 'https://%s' % (match.group(1).replace("\\", "").replace("u003d", "="))
        #print(image_link)

        file_name = '%s.jpg' % (uuid.uuid5(uuid.NAMESPACE_DNS, image_link))
        print(file_name)

        file_path = os.path.join(img_path, file_name)

        if not os.path.exists(file_path):
            req = requests.get(image_link, stream=True)
            if req.status_code == 200:
                with open(file_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(req.raw, f)

            # check if it is image or not
            try:
                im = Image.open(file_path)
            except OSError:
                if os.path.exists(file_path):
                    os.remove(file_path)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    main(config=config)
