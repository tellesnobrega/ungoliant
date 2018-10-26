import configparser
import os

import bugzilla
from trello import TrelloClient


_conf_dir = os.path.join(os.environ['HOME'], '.ungoliant')
_conf_fp = os.path.join(_conf_dir, 'config.ini')


cache_dir = os.path.join(_conf_dir, 'cache')


config = configparser.ConfigParser()
config.read(_conf_fp)


bz_client = bugzilla.Bugzilla('bugzilla.redhat.com')
_bz_args = [config['BUGZILLA']['USER'], config['BUGZILLA']['PASS']]
_bz_args = _bz_args if (_bz_args) else []
bz_client.interactive_login(*_bz_args)


trello_client = TrelloClient(api_key=config['TRELLO']['APP_KEY'],
                             token=config['TRELLO']['TOKEN'])
