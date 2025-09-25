import argparse
import os
import torch
import torch.nn.functional as F
from models import Model

from torch_geometric.loader import DataLoader
from torch_geometric.datasets import TUDataset

from sklearn.metrics import f1_score, precision_recall_fscore_support, classification_report
from torch.utils.data import random_split

from torchmetrics import ConfusionMatrix

from datetime import datetime
from util_logger import set_logger

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=777, help='random seed')
parser.add_argument('--batch_size', type=int, default=512, help='batch size')
parser.add_argument('--lr', type=float, default=0.001, help='learning rate')
parser.add_argument('--weight_decay', type=float, default=0.001, help='weight decay')
parser.add_argument('--nhid', type=int, default=128, help='hidden size')
parser.add_argument('--sample_neighbor', type=bool, default=True, help='whether sample neighbors')
parser.add_argument('--sparse_attention', type=bool, default=True, help='whether use sparse attention')
parser.add_argument('--structure_learning', type=bool, default=True, help='whether perform structure learning')
parser.add_argument('--pooling_ratio', type=float, default=0.5, help='pooling ratio')
parser.add_argument('--dropout_ratio', type=float, default=0.0, help='dropout ratio')
parser.add_argument('--lamb', type=float, default=1.0, help='trade-off parameter')
parser.add_argument('--device', type=str, default='cuda:0', help='specify cuda devices')

parser.add_argument('--save_dir', type=str, default='/workspace/run/HGP-SL/test')
parser.add_argument('--src_dir', type=str, default='/workspace/data/dataset')
parser.add_argument('--dataset', type=str, default='nia80')
parser.add_argument('--model', type=str, default='/workspace/run/HGP-SL/train/best_model.pth', help='DD/PROTEINS/NCI1/NCI109/Mutagenicity/ENZYMES')

args = parser.parse_args()
torch.manual_seed(args.seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(args.seed)

os.makedirs(args.save_dir, exist_ok=True)

LOGGER = set_logger(args.save_dir, log_name=f'{datetime.now().strftime("%y%m%d_%H%M%S")}_test_log', is_stream=True)

LOGGER.info('START')
LOGGER.info(f'python HGP-SL/test.py --src_dir /workspace/data/dataset --save_dir /workspace/run/HGP-SL/test --dataset nia80 --model /workspace/run/HGP-SL/train/best_model.pth')
LOGGER.info(args)

test_set = TUDataset(os.path.join(args.src_dir, 'test','hgpsl', args.dataset),name=args.dataset,use_node_attr=True)

args.num_classes = test_set.num_classes
args.num_features = test_set.num_features

test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False)

model = Model(args).to(args.device)
optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

def compute_test(loader):
    model.eval()
    correct = 0.0
    loss_test = 0.0
    all_predictions = [] 
    all_labels = []
    # LOGGER.info(f'{loader}')
    for i,(data) in enumerate(loader):
        data = data.to(args.device)
        out = model(data)
        pred = out.max(dim=1)[1]
        correct += pred.eq(data.y).sum().item()
        loss_test += F.nll_loss(out, data.y).item()
        # f1-score
        pred_list = pred.tolist()
        gt_list = data.y.tolist()
        for idx in range(len(pred_list)):
            tmp_i = (i*args.batch_size)+idx
            all_predictions.append(pred_list[idx])
            all_labels.append(gt_list[idx])
            calc = classification_report(all_labels, all_predictions, output_dict = True, zero_division = 1)

        # confusion matrix
            cnf_mt = ["", "", "", "", "", ""]
            acm_cnf_mt = [[0, 0, 0, 0, 0,0],[0, 0, 0, 0, 0,0],[0, 0, 0, 0, 0,0],
                          [0, 0, 0, 0, 0,0],[0, 0, 0, 0, 0,0],[0, 0, 0, 0, 0,0]]
            for label in range(6):
                if gt_list[idx] == label and pred_list[idx] == label:
                    cnf_mt[label] = "TP"
                    acm_cnf_mt[label][0] += 1
                elif gt_list[idx] != pred_list[idx] and gt_list[idx] == label:
                    cnf_mt[label] = "FN"
                    acm_cnf_mt[label][3] += 1
                elif gt_list[idx] != pred_list[idx] and pred_list[idx] == label:
                    cnf_mt[label] = "FP"
                    acm_cnf_mt[label][2] += 1
                else:
                    cnf_mt[label] = "TN"
                    acm_cnf_mt[label][1] += 1
#                if str(label) not in calc:
#                    calc.setdefault(str(label), {'support': 0, 'accuracy' : 0})
                acm_cnf_mt[label][4] = (acm_cnf_mt[label][0] + acm_cnf_mt[label][1]) / (acm_cnf_mt[label][0]+acm_cnf_mt[label][1]+acm_cnf_mt[label][2]+acm_cnf_mt[label][3])

            log_str = f'{tmp_i} :: [GT : {gt_list[idx]}] : [pred : {pred_list[idx]}] \n'
            log_str += f'0 (FL) :: {cnf_mt[0]} TP : {acm_cnf_mt[0][0]} TN : {acm_cnf_mt[0][1]} FP : {acm_cnf_mt[0][2]} FN : {acm_cnf_mt[0][3]}\n' # Acc : {acm_cnf_mt[0][4]}
            log_str += f'1 (FR) :: {cnf_mt[1]} TP : {acm_cnf_mt[1][0]} TN : {acm_cnf_mt[1][1]} FP : {acm_cnf_mt[1][2]} FN : {acm_cnf_mt[1][3]}\n'
            log_str += f'2 (FU) :: {cnf_mt[2]} TP : {acm_cnf_mt[2][0]} TN : {acm_cnf_mt[2][1]} FP : {acm_cnf_mt[2][2]} FN : {acm_cnf_mt[2][3]}\n' 
            log_str += f'3 (NS) :: {cnf_mt[3]} TP : {acm_cnf_mt[3][0]} TN : {acm_cnf_mt[3][1]} FP : {acm_cnf_mt[3][2]} FN : {acm_cnf_mt[3][3]}\n'
            log_str += f'4 (OU) :: {cnf_mt[4]} TP : {acm_cnf_mt[4][0]} TN : {acm_cnf_mt[4][1]} FP : {acm_cnf_mt[4][2]} FN : {acm_cnf_mt[4][3]}\n'
            log_str += f'5 (SA) :: {cnf_mt[5]} TP : {acm_cnf_mt[5][0]} TN : {acm_cnf_mt[5][1]} FP : {acm_cnf_mt[5][2]} FN : {acm_cnf_mt[5][3]}\n'
            log_str += f'accumulated accuracy :: {calc["accuracy"]}'

            LOGGER.info(log_str)

    confmat = ConfusionMatrix(task='multiclass', num_classes=6)
    LOGGER.info(confmat(torch.tensor(all_predictions), torch.tensor(all_labels)))

    # f1 = f1_score(all_labels, all_predictions, average='weighted')
    return correct / len(loader.dataset), loss_test #, f1


if __name__ == '__main__':
    # Restore best model for test set
    model.load_state_dict(torch.load(args.model))
    test_acc, test_loss = compute_test(test_loader)

    LOGGER.info(f'Test set results, loss = {test_loss:.6f}, accuracy = {test_acc:.6f}')