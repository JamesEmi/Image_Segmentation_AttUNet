import os
import argparse
import random
import shutil
from shutil import copyfile
from misc import printProgressBar


def rm_mkdir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print('Remove path - %s'%dir_path)
    os.makedirs(dir_path)
    print('Create path - %s'%dir_path)

def main(config):

    rm_mkdir(config.train_path)
    rm_mkdir(config.train_GT_path)
    rm_mkdir(config.valid_path)
    rm_mkdir(config.valid_GT_path)
    rm_mkdir(config.test_path)
    rm_mkdir(config.test_GT_path)
    
    #WHY is the code deleting these dirs??

    filenames = os.listdir(config.origin_data_path)
    data_list = []
    GT_list = []

    for filename in filenames:
        ext = os.path.splitext(filename)[-1]
        if ext =='.jpg':
            # print('here')
            # filename = filename.split('_')[-1][:-len('.jpg')]
            filename = filename[:-len('.jpg')]
            # entirely unnecessay antics 101. Or is there value in having the 'segmentation' suffix in mask files?
            # data_list.append('ISIC_'+filename+'.jpg')
            # GT_list.append('ISIC_'+filename+'_segmentation.png')
            data_list.append(filename+'.jpg')
            GT_list.append(filename+'.png')
            
            #change this acc to my LSU dataset. In my case it's just named by the original filename! Bad practice?

    num_total = len(data_list)
    num_train = int((config.train_ratio/(config.train_ratio+config.valid_ratio+config.test_ratio))*num_total)
    num_valid = int((config.valid_ratio/(config.train_ratio+config.valid_ratio+config.test_ratio))*num_total)
    num_test = num_total - num_train - num_valid

    print('\nNum of train set : ',num_train)
    print('\nNum of valid set : ',num_valid)
    print('\nNum of test set : ',num_test)

    Arange = list(range(num_total))
    random.shuffle(Arange)

    for i in range(num_train):
        idx = Arange.pop()
        
        src = os.path.join(config.origin_data_path, data_list[idx])
        print(config.origin_data_path)
        dst = os.path.join(config.train_path,data_list[idx])
        print(config.train_path)
        copyfile(src, dst)
        
        src = os.path.join(config.origin_GT_path, GT_list[idx])
        dst = os.path.join(config.train_GT_path, GT_list[idx])
        copyfile(src, dst)

        printProgressBar(i + 1, num_train, prefix = 'Producing train set:', suffix = 'Complete', length = 50)
        

    for i in range(num_valid):
        idx = Arange.pop()

        src = os.path.join(config.origin_data_path, data_list[idx])
        dst = os.path.join(config.valid_path,data_list[idx])
        copyfile(src, dst)
        
        src = os.path.join(config.origin_GT_path, GT_list[idx])
        dst = os.path.join(config.valid_GT_path, GT_list[idx])
        copyfile(src, dst)

        printProgressBar(i + 1, num_valid, prefix = 'Producing valid set:', suffix = 'Complete', length = 50)

    for i in range(num_test):
        idx = Arange.pop()

        src = os.path.join(config.origin_data_path, data_list[idx])
        dst = os.path.join(config.test_path,data_list[idx])
        copyfile(src, dst)
        
        src = os.path.join(config.origin_GT_path, GT_list[idx])
        dst = os.path.join(config.test_GT_path, GT_list[idx])
        copyfile(src, dst)


        printProgressBar(i + 1, num_test, prefix = 'Producing test set:', suffix = 'Complete', length = 50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    
    # model hyper-parameters
    parser.add_argument('--train_ratio', type=float, default=0.8)
    parser.add_argument('--valid_ratio', type=float, default=0.1)
    parser.add_argument('--test_ratio', type=float, default=0.1)

    # data path
    parser.add_argument('--origin_data_path', type=str, default='../ISIC/dataset/ISIC2018_Task1-2_Training_Input')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/train/image
    parser.add_argument('--origin_GT_path', type=str, default='../ISIC/dataset/ISIC2018_Task1_Training_GroundTruth')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/train/mask
    
    parser.add_argument('--train_path', type=str, default='./dataset/train/')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/train/image
    parser.add_argument('--train_GT_path', type=str, default='./dataset/train_GT/')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/train/mask
    parser.add_argument('--valid_path', type=str, default='./dataset/valid/')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/train/image
    parser.add_argument('--valid_GT_path', type=str, default='./dataset/valid_GT/')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/val/mask
    parser.add_argument('--test_path', type=str, default='./dataset/test/')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/val/image
    parser.add_argument('--test_GT_path', type=str, default='./dataset/test_GT/')
    # /notebooks/pleural_line_segment/init_play/baby_dataset/val/mask

    config = parser.parse_args()
    print(config)
    main(config)
