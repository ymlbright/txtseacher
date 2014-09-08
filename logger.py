#-*- coding: utf-8 -*-

import logging
import sys

logger = logging.getLogger("MySeacher")
formatter = logging.Formatter('[%(asctime)s] %(message)s', \
			'%H:%M:%S')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.setLevel(logging.WARNING)
logger.addHandler(stream_handler)

output = logging.getLogger("Searchresult")
output_handler = logging.StreamHandler(sys.stdout)
output_handler.setFormatter(logging.Formatter('%(message)s'))
output_handler.setLevel(logging.INFO)
output.setLevel(logging.INFO)
output.addHandler(output_handler)