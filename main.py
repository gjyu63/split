import argparse


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True)
    ap.add_argument("-p", "--train", required=True,
                    help="ratio of training dataset")
    ap.add_argument("-v", "--val", required=True,
                    help="ratio of validation dataset")
    ap.add_argument("-t", "--test", required=True,
                    help="ratio of testing dataset")
    args = vars(ap.parse_args())

    train, val, test, dirr = float(args['train']), float(args['val']), float(args['test']), args['dir']

    train_t = train / (train + val + test)
    val_t = val / (train + val + test)
    test_t = test / (train + val + test)

    split(dirr, train_t, val_t, test_t)


def split(dirr, train, val, test):
    import math
    import os as macOS
    from os import walk
    dir_lst = []

    for (_, dirnames, _) in walk(dirr):
        dir_lst += dirnames
    try:
        for target in ['train', 'val', 'test']:
            for category in dir_lst:
                macOS.makedirs(macOS.path.join(dirr, target, category))
    except FileExistsError:
        print('dir exists. skipped mkdir')

    for category in dir_lst:
        # cd into that dir, split, copy to the dest
        file_lst = macOS.listdir(macOS.path.join(dirr, category))
        train_r = math.floor(train * len(file_lst))
        val_r = math.floor(val * len(file_lst))
        test_r = math.floor(test * len(file_lst))

        train_lst = file_lst[:train_r]
        val_lst = file_lst[train_r: train_r + val_r]
        test_lst = file_lst[train_r + val_r:]

        # copy to the new dest
        from shutil import copyfile

        try:
            for f in train_lst:
                print('copying ' + macOS.path.join(dirr, category, f) + ' to ' + macOS.path.join(dirr, 'train', category, f))
                copyfile(macOS.path.join(dirr, category, f), macOS.path.join(dirr, 'train', category, f))

            for f in val_lst:
                print('copying ' + macOS.path.join(dirr, category, f) + ' to ' + macOS.path.join(dirr, 'val', category, f))
                copyfile(macOS.path.join(dirr, category, f), macOS.path.join(dirr, 'val', category, f))

            for f in test_lst:
                print('copying ' + macOS.path.join(dirr, category, f) + ' to ' + macOS.path.join(dirr, 'test', category, f))
                copyfile(macOS.path.join(dirr, category, f), macOS.path.join(dirr, 'test', category, f))
        except IsADirectoryError:
            print('skipped' + macOS.path.join(dirr, category, f) + ' because it\'s a directory')



if __name__ == '__main__':
    main()