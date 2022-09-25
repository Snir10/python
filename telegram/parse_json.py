# parsing channel messages in order to get img ID
## https://api.telegram.org/bot<token>/getFile?file_id=<file_id>
## From the result you need the file_path and you then got the image location https://api.telegram.org/file/bot<token>/<file_path>

import json
import os

# some JSON:



with open('/Users/user/Desktop/github projects/python/telegram/channel_messages0.json', 'r') as fcc_file:
    fcc_data = json.load(fcc_file)
    #print(fcc_data)
    #print(json.dumps(fcc_data, indent=8, sort_keys=True))
    print(fcc_data[6])

    x = fcc_data[6]
    id = fcc_data[6].get('media').get('photo').get('id')

print(int(id))



    #print(fcc_data[6]['message'])
    #print(fcc_data[6]['media'].keys())


