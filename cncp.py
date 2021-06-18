import argparse
import os
import shutil


def copy_file(dir_in, dir_out):
    shutil.rmtree(dir_out, ignore_errors=True)
    shutil.copytree(dir_in, dir_out)


def main():
    parser = argparse.ArgumentParser(description='CNCP Website Generator')
    parser.add_argument('src', type=str, metavar='src')
    parser.add_argument('dst', type=str, metavar='dst')
    args = parser.parse_args()
    copy_file(os.path.join(args.src, 'file'), args.dst)


if __name__ == '__main__':
    main()
