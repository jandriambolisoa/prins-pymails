#
# This templates folder must includes the template mails you need
# 
# template_name
# -- images
# ---- yourimages.png
# -- content.html
# -- content.txt
# -- datas.json
#
# The datas.json file contains Subject:str and constants:dict
# 

import os
__TEMPLATES_FOLDER__ = os.path.normpath(os.path.split(__file__)[0])