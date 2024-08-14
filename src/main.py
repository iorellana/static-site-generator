from os import listdir, mkdir
from os.path import exists, join, isfile
from shutil import copy, rmtree

def main():
    # copy everything from static to public
    static_dir = "static"
    public_dir = "public"
    if exists(public_dir):
        rmtree(public_dir)
    mkdir(public_dir)
    copy_recursive(static_dir, public_dir)

def copy_recursive(src, dst):
    if isfile(src):
        copy(src, dst)
    else:
        if not exists(dst):
            mkdir(dst)
        for l in listdir(src):
            copy_recursive(join(src, l), join(dst, l))

main()