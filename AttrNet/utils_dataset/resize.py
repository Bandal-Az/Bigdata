import os
from PIL import Image

with open("/workspace/yolov5/all_json_list.txt", 'r') as f :
    data = f.readlines()
    
for i in range(len(data)) :
    data[i] = data[i].split('.')[0] + ".jpg"
    
root_dir = "/workspace/data/"

os.makedirs(root_dir + "jpg-480/train/", exist_ok=True)

for line in data :
    print(line)
    img = Image.open(root_dir + "jpg/train/" + line)
    new_img = img.resize((480, 270))
    new_img.save(root_dir + "jpg-480/train/" + line)