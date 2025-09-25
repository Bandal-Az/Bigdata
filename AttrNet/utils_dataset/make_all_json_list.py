import os

list_data = os.listdir('/workspace/data/json')

with open('all_json_list.txt', 'w', encoding='utf-8') as f:
    f.writelines('\n'.join(list_data))