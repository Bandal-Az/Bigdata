import argparse
import os
import time
import torch
import torch.nn.functional as F
from models import Model

from torch_geometric.loader import DataLoader
from torch_geometric.datasets import TUDataset

from tensorboardX import SummaryWriter

from datetime import datetime
from util_logger import set_logger

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=777, help='random seed')
parser.add_argument('--batch_size', type=int, default=256, help='batch size')
parser.add_argument('--lr', type=float, default=0.001, help='learning rate')
parser.add_argument('--weight_decay', type=float, default=0.0001, help='weight decay')
parser.add_argument('--nhid', type=int, default=128, help='hidden size')
parser.add_argument('--sample_neighbor', type=bool, default=True, help='whether sample neighbors')
parser.add_argument('--sparse_attention', type=bool, default=True, help='whether use sparse attention')
parser.add_argument('--structure_learning', type=bool, default=True, help='whether perform structure learning')
parser.add_argument('--pooling_ratio', type=float, default=0.5, help='pooling ratio')
parser.add_argument('--dropout_ratio', type=float, default=0.0, help='dropout ratio')
parser.add_argument('--lamb', type=float, default=1.0, help='trade-off parameter')
parser.add_argument('--device', type=str, default='cuda:0', help='specify cuda devices')
parser.add_argument('--epochs', type=int, default=100, help='maximum number of epochs')
parser.add_argument('--patience', type=int, default=10, help='patience for early stopping')

parser.add_argument('--save_dir', type=str, default='/workspace/run/HGP-SL/train')
parser.add_argument('--src_dir', type=str, default='/workspace/data/dataset')
parser.add_argument('--dataset', type=str, default='nia80')

args = parser.parse_args()

os.makedirs(args.save_dir, exist_ok=True)

save_last_model_path = os.path.join(args.save_dir, f'last_model.pth')
save_best_model_path = os.path.join(args.save_dir, f'best_model.pth')

LOGGER = set_logger(args.save_dir, log_name=f'{datetime.now().strftime("%y%m%d_%H%M%S")}_train_log', is_stream=True)

tb_path = os.path.join(args.save_dir, 'tensorboard')
tb_train_writer = SummaryWriter(os.path.join(tb_path, 'train'))
tb_val_writer = SummaryWriter(os.path.join(tb_path, 'val'))

torch.manual_seed(args.seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(args.seed)

LOGGER.info('START')
LOGGER.info(args)

train_set = TUDataset(os.path.join(args.src_dir, 'train','hgpsl', args.dataset),name=args.dataset,use_node_attr=True)
val_set = TUDataset(os.path.join(args.src_dir, 'val','hgpsl', args.dataset),name=args.dataset,use_node_attr=True)
test_set = TUDataset(os.path.join(args.src_dir, 'test','hgpsl', args.dataset),name=args.dataset,use_node_attr=True)

args.num_classes = train_set.num_classes
args.num_features = train_set.num_features

LOGGER.info(f'DATASET : Train {len(train_set)} | Validation {len(val_set)} | Test {len(test_set)}')

train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False)
test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False)

model = Model(args).to(args.device)
optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

def train():
    check = 0
    patience_cnt = 0
    val_check_values = []
    best_epoch = 0

    t = time.time()
    model.train()
    for epoch in range(args.epochs):
        current_lr = optimizer.state_dict()['param_groups'][0]['lr']
        loss_train = 0.0
        correct = 0
        for i, data in enumerate(train_loader):
            optimizer.zero_grad()
            data = data.to(args.device)
            out = model(data)
            loss = F.nll_loss(out, data.y)
            loss.backward()
            optimizer.step()
            loss_train += loss.item()
            pred = out.max(dim=1)[1]
            correct += pred.eq(data.y).sum().item()
        acc_train = correct / len(train_loader.dataset)
        acc_val, loss_val = compute_test(val_loader)

        tb_train_writer.add_scalar('train/loss', loss_train, epoch)        
        tb_train_writer.add_scalar('train/acc', acc_train, epoch)

        tb_val_writer.add_scalar('val/loss', loss_val, epoch)        
        tb_val_writer.add_scalar('val/acc', acc_val, epoch)     
        # tb_val_writer.add_scalar('val/f1-score', f1_val, epoch)

        LOGGER.info(f'Epoch: {epoch + 1:04d} loss_train: {loss_train:.6f} acc_train: {acc_train:.6f} loss_val: {loss_val:.6f} acc_val: {acc_val:.6f}') # f1_val:{f1_val:.6f}')

        val_check_values.append(acc_val)
        torch.save(model.state_dict(), save_last_model_path)
        if val_check_values[-1] > check:
            check = val_check_values[-1]
            best_epoch = epoch
            LOGGER.info(f'@ Best Epoch: {epoch + 1:04d} ... acc:{acc_val:.6f}')
            torch.save(model.state_dict(), save_best_model_path)
            patience_cnt = 0
        else:
            patience_cnt += 1

        if patience_cnt == args.patience:
            break

    LOGGER.info(f'Optimization Finished! Total time elapsed: {time.time() - t:.6f}')

    return best_epoch

def compute_test(loader):
    model.eval()
    correct = 0.0
    loss_test = 0.0

    for data in loader:
        data = data.to(args.device)
        out = model(data)
        pred = out.max(dim=1)[1]
        correct += pred.eq(data.y).sum().item()
        loss_test += F.nll_loss(out, data.y).item()
        # # f1-score
        # all_predictions.extend(pred.cpu().numpy())
        # all_labels.extend(data.y.cpu().numpy())

    # f1 = f1_score(all_labels, all_predictions, average='weighted')
    return correct / len(loader.dataset), loss_test #, f1

if __name__ == '__main__':
    # Model training
    best_model = train()
    # Restore best model for test set
    model.load_state_dict(torch.load(save_best_model_path))
    test_acc, test_loss = compute_test(test_loader)
    LOGGER.info(f'Test set results, loss = {test_loss:.6f}, accuracy = {test_acc:.6f}')