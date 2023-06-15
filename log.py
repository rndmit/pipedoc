import logging
import sys

log = logging.Logger("main")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)