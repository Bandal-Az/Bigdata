import os
import os.path

dir_path = '/workspace/data/jpg-480'

train_set = [ path[:-4] for path in os.listdir('/workspace/data/jpg-480/train') if os.path.splitext(path)[1] == '.jpg']
val_set = [ path[:-4] for path in os.listdir('/workspace/data/jpg-480/val') if os.path.splitext(path)[1] == '.jpg']
test_set = [ path[:-4] for path in os.listdir('/workspace/data/jpg-480/test') if os.path.splitext(path)[1] == '.jpg']
print(f'Train [{len(train_set)}] | Validation [{len(val_set)}] | Test [{len(test_set)}]')

with open('/workspace/attnet/annotations/train.txt','w', encoding='utf-8') as f:
    f.writelines('\n'.join(train_set))
with open('/workspace/attnet/annotations/val.txt','w', encoding='utf-8') as f:
    f.writelines('\n'.join(val_set))
with open('/workspace/attnet/annotations/test.txt','w', encoding='utf-8') as f:
    f.writelines('\n'.join(test_set))
print(f'Saved Dataset List : /workspace/attnet/annotations/(set).txt')