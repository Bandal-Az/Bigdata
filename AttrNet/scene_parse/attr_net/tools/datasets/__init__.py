import os
from torch.utils.data import DataLoader
from .nia80_object import BasketballDataset

def get_dataset(opt, split):
    if opt.dataset == 'nia80':
        if split == 'train':
            img_dir = os.path.join(opt.dataset_dir,opt.train_img_dir)
            ann_apth = os.path.join(opt.dataset_dir, opt.train_ann_path)

            ds = BasketballDataset(ann_apth, img_dir, split='train',
                                    concat_img=opt.concat_img)
        elif split == 'val':
            img_dir = os.path.join(opt.dataset_dir,opt.val_img_dir)
            ann_apth = os.path.join(opt.dataset_dir, opt.val_ann_path)
            
            ds = BasketballDataset(ann_apth, img_dir, split='val',concat_img=opt.concat_img)
        elif split == 'test':
            img_dir = os.path.join(opt.dataset_dir,opt.test_img_dir)
            ann_apth = os.path.join(opt.dataset_dir, opt.test_ann_path)
            
            ds = BasketballDataset(ann_apth, img_dir,split='test',concat_img=opt.concat_img)
        else:
            raise ValueError('Invalid dataset split: %s' % split)
    return ds


def get_dataloader(opt, split):
    ds = get_dataset(opt, split)
    loader = DataLoader(dataset=ds, batch_size=opt.batch_size,
                        num_workers=opt.num_workers, shuffle=opt.shuffle_data)
    return loader