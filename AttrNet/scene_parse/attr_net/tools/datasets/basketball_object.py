import os
import json

import numpy as np
import cv2
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import pycocotools.mask as mask_util

class BasketballDataset(Dataset):

    def __init__(self, obj_ann_path, img_dir, split,
                 min_img_id=None, max_img_id=None, concat_img=True):
        
        with open(obj_ann_path, 'r') as f: 
            anns = json.load(f)

        self.obj_masks = anns['object_masks']
        self.img_name = anns['image_name']

        self.img_ids = anns['image_idxs']
        # self.cat_ids = anns['category_idxs'][min_id: max_id]
        
        if anns['feature_vectors'] != []: #@ feature vec -> np.array
            self.feat_vecs = np.array(anns['feature_vectors']).astype(float)
        else:
            self.feat_vecs = None
            
        self.split=split
        self.img_dir = img_dir
        self.concat_img = concat_img
        transform_list = [transforms.ToTensor()]
        self._transform = transforms.Compose(transform_list)
        
    def __len__(self):
        return len(self.img_name)
    
    def __getitem__(self, idx):
        img_name =self.img_name[idx]+".jpg"
        img = cv2.imread(os.path.join(self.img_dir, self.split, img_name), cv2.IMREAD_COLOR) 
        img = self._transform(img) #@ transforms.ToTensor()
        label = -1 
        if self.feat_vecs is not None:
            label = torch.Tensor(self.feat_vecs[idx])
       
##########! pixel masking with bbox ####################################
        xmax, ymax, xmin, ymin = self.obj_masks[idx]["counts"]   ### box_coords = [x1, y1, x2, y2]
        # img_w, img_h = self.obj_masks[idx]["size"]
        img_w, img_h = 480, 270
        mask = np.zeros((img_w, img_h), dtype=float)  #* mask = (1920, 1080)
        
        if xmax > 480 :
            xmax == 480
        
        for x_idx in range(xmin - 1, xmax) :
            for y_idx in range(ymin - 1, ymax) :
                mask[x_idx, y_idx] = 1.0
        
        mask = mask.transpose()   #* img.shape = (1080, 1920)
        
        seg = img.clone()
        for i in range(3):
            seg[i, :, :] = img[i, :, :] * mask  #! masking, * in numpy == element-wise mult
#!################################################################################

        resize_h, resize_w = 270, 480      #@ for resizing
                
        transform_list = [transforms.ToPILImage(),
                          transforms.ToTensor(),
                        #   transforms.Resize((resize_h, resize_w)),   #*## 1080, 1920 -> 270, 480
                          transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])]
        if self.concat_img:
            data = img.clone().resize_(6, resize_h, resize_w).fill_(0) #! make 6 channel
            data[0:3] = transforms.Compose(transform_list)(seg)
            data[3:6] = transforms.Compose(transform_list)(img)
        else:
            data = img.clone().resize_.fill_(0)
            data[:, :, :] = transforms.Compose(transform_list)(seg)
        
        return data, label