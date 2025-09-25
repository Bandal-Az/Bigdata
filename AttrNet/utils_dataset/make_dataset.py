import os
import os.path
import natsort
import random
import shutil

random.seed(1)

img_dir = '/workspace/data/jpg-480'
train_ratio = 0.8
val_ratio = 0.1

class_check = {}
img_list = []

for root, dir, files in os.walk(img_dir):
    for file in files:
        file_name, file_ext = os.path.splitext(file)
        if file_ext.lower() == '.jpg' and file_name not in img_list:
            img_list.append(file_name)

print(len(img_list))

for image_name in img_list:
    class_name = image_name[:8]
    if class_name not in class_check:
        class_check[class_name] = []
    class_check[class_name].append(image_name)

dataset = {}

for key, val in class_check.items():
    dataset[key] = {}
    tmp = natsort.natsorted(val)
    file_cnt = len(tmp)
    random.shuffle(tmp)

    train_cnt = int(file_cnt * train_ratio)
    val_cnt = int(file_cnt * val_ratio)
    
    dataset[key]['train'] = tmp[:train_cnt]
    dataset[key]['val'] = tmp[train_cnt:train_cnt+val_cnt]
    dataset[key]['test'] = tmp[train_cnt+val_cnt:]

    print(f'{key} :: {len(dataset[key]["train"])} | {len(dataset[key]["val"])} | {len(dataset[key]["test"])}')

    for key, val in dataset[key].items():
        os.makedirs(os.path.join(img_dir, key), exist_ok=True)
        for filename in val:
            shutil.move(os.path.join(img_dir, f'{filename}.jpg'), os.path.join(img_dir, key, f'{filename}.jpg'))