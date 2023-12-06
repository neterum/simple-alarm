import logging
import logging.config
import strings

class Log:
    def __init__(self):
        # self.homeFolderLocation = "~/.config/simple-alarm/logs/"

        # logging.basicConfig(filename=strings.CONFIG_FILE_LOCATION, encoding='utf-8', level=logging.DEBUG,
        #                     format='%(asctime)s%(levelname)s:%(message)s')
        logging.config.fileConfig("logging.yaml")
        logger = logging.getLogger("mainLogger")
        logger.debug('debug message')