import random
from os import listdir, makedirs, remove
from os.path import exists, basename, join
from random import sample
from PyQt5.QtCore import QThread, pyqtSignal


def check(dir=''):
    if not exists(dir):
        makedirs(dir)


def get_file_list(path=''):
    img_dir = join(path, 'images')
    label_dir = join(path, 'labels')
    # print(img_dir,label_dir)
    if exists(img_dir) and exists(label_dir):
        img_list = listdir(img_dir)
        label_list = listdir(label_dir)
        return ([join(img_dir, i) for i in img_list], [join(label_dir, j) for j in label_list])
    else:
        return ([], [])


def output_split_txt(set=[], set_name='', output='./', img_dir='./'):
    if exists(join(output, set_name + '.txt')):
        remove(join(output, set_name + '.txt'))
    for s in set:
        with open(join(output, set_name + '.txt'), 'a+', encoding='utf8') as fp:
            fp.write(join(img_dir, s + '.jpg').replace('\\', '/'))
            fp.write('\n')


class SplitDataset(QThread):
    result_ready = pyqtSignal(dict)
    def __init__(self, inputDir='./', outputDir='./', percents=[0.75, 0.15, 0.10], seed=50):
        super(SplitDataset, self).__init__()
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.percents = percents
        self.seed = seed
        check(inputDir)
        check(outputDir)

    def split(self):
        img_list, label_list = get_file_list(path=self.inputDir)
        if len(label_list) == 0:
            print('标签为空')
            return {'train_num': 0, 'val_num': 0, 'test_num': 0}
        else:
            filenames = []
            for i, label in enumerate(label_list):
                filenames.append(basename(label).split('.')[0])
            train_num = int(self.percents[0] * len(filenames))
            val_num = int(self.percents[1] * len(filenames))
            test_num = len(filenames) - (train_num + val_num)
            random.seed(self.seed)
            train_set = sample(filenames, train_num)
            val_test_set = []
            test_set = []
            for f in filenames:
                if f not in train_set:
                    val_test_set.append(f)
            val_set = sample(val_test_set, val_num)
            for f in val_test_set:
                if f not in val_set:
                    test_set.append(f)
            output_split_txt(train_set, set_name='train', output=self.outputDir, img_dir=join(self.inputDir, 'images'))
            output_split_txt(val_set, set_name='val', output=self.outputDir, img_dir=join(self.inputDir, 'images'))
            output_split_txt(test_set, set_name='test', output=self.outputDir, img_dir=join(self.inputDir, 'images'))
            return {'train_num': len(train_set), 'val_num': len(val_set), 'test_num': len(test_set)}

    def run(self):
        data_dict = self.split()
        self.result_ready.emit(data_dict)


if __name__ == '__main__':
    dataset = SplitDataset(inputDir=r'C:\Users\XiaoS\Desktop\桌面\boat')
    print(dataset.split())
