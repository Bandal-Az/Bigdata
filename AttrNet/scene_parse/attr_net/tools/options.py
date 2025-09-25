import argparse
import os
import utils as utils
import torch


class BaseOptions():

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.initialized = False
        
    def initialize(self):
        self.parser.add_argument('--run_dir', default='/workspace/AttrNet/run/test', type=str, help='experiment directory')
        self.parser.add_argument('--dataset', default='nia80', type=str, help='dataset')
        self.parser.add_argument('--load_checkpoint_path', default=None, type=str, help='load checkpoint path')
        self.parser.add_argument('--gpu_ids', default='0', type=str, help='ids of gpu to be used')

        self.parser.add_argument('--dataset_dir', default='/workspace/data/dataset')

        self.parser.add_argument('--concat_img', default=1, type=int, help='concatenate original image when sent to network')
        # self.parser.add_argument('--split_id', default=3500, type=int, help='splitting index between train and val images')
        self.parser.add_argument('--batch_size', default=16, type=int, help='batch size')
        self.parser.add_argument('--num_workers', default=4, type=int, help='number of workers for loading')
        self.parser.add_argument('--learning_rate', default=0.002, type=float, help='learning rate')
        #@@@@@@@@@@@@@@@@@@@@@@@@@      DONT TOUCH@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self.parser.add_argument('--world_size', default=1, type=int,
                        help='number of distributed processes')
        self.parser.add_argument('--local_rank', type=int)
        self.parser.add_argument('--dist_url', default='env://',
                        help='url used to set up distributed training')
        self.initialized = True
        #@@@@@@@@@@@@@@@@@@@@@@@@@      DONT TOUCH@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self.parser.add_argument("--feature_vector_len",default=26, type=int, help='for model\'s output layer')  #^## for model.py initializing output layer
        
    def parse(self):
        # initialize parser
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()

        self.opt.gpu = 'cuda'
        # parse gpu id list
        # str_gpu_ids = self.opt.gpu_ids.split(',')
        # self.opt.gpu_ids = []
        # for str_id in str_gpu_ids:
        #     if str_id.isdigit() and int(str_id) >= 0:
        #         self.opt.gpu_ids.append(int(str_id))
        # if len(self.opt.gpu_ids) > 0 and torch.cuda.is_available():
        #     torch.cuda.set_device(self.opt.gpu_ids[0])
        # else:
        #     print('| using cpu')
        #     self.opt.gpu_ids = []

        # print and save options
        args = vars(self.opt)
        print('| options')
        for k, v in args.items():
            print('%s: %s' % (str(k), str(v)))
        if not os.path.isdir(self.opt.run_dir) :
            utils.mkdirs(self.opt.run_dir)

        if self.is_train:
            filename = 'train_opt.txt'
        else:
            filename = 'test_opt.txt'
        file_path = os.path.join(self.opt.run_dir, filename)
        with open(file_path, 'wt') as fout:
            fout.write('| options\n')
            for k, v in sorted(args.items()):
                fout.write('%s: %s\n' % (str(k), str(v)))

        return self.opt


class TrainOptions(BaseOptions):

    def initialize(self):
        BaseOptions.initialize(self)

        self.parser.add_argument('--train_img_dir', default='train/images')
        self.parser.add_argument('--train_ann_path', default='train/attrnet_label/attribute_annotation.json')
        self.parser.add_argument('--val_img_dir', default='val/images')
        self.parser.add_argument('--val_ann_path', default='val/attrnet_label/attribute_annotation.json')

        self.parser.add_argument('--num_iters', default=100, type=int, help='total number of iterations')
        self.parser.add_argument('--display_every', default=20, type=int, help='display training information every N iterations')
        self.parser.add_argument('--checkpoint_every', default=1000, type=int, help='save every N iterations')
        self.parser.add_argument('--val_epochs', default=20, type=int, help='do validation')    #^## for validation per k epochs
        self.parser.add_argument('--shuffle_data', default=1, type=int, help='shuffle dataloader')
        self.is_train = True


class TestOptions(BaseOptions):

    def initialize(self):
        BaseOptions.initialize(self)
        self.parser.add_argument('--test_img_dir', default='test/images')
        self.parser.add_argument('--test_ann_path', default='test/attrnet_label/attribute_annotation.json')

        self.parser.add_argument('--split', default='test')

        self.parser.add_argument('--output_path', default='result.json', type=str, help='save path for derendered scene annotation')
        self.parser.add_argument('--shuffle_data', default=0, type=int, help='shuffle dataloader')
        self.parser.add_argument('--use_cat_label', default=1, type=int, help='use object detector class label')
        self.is_train = False


def get_options(mode):
    if mode == 'train':
        opt = TrainOptions().parse()
    elif mode == 'test':
        opt = TestOptions().parse()
    else:
        raise ValueError('Invalid mode for option parsing: %s' % mode)
    return opt