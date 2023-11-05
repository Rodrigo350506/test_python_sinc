import os
import shutil
import argparse
import time
import logging

def sync_folders(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            sync_folders(s, d)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
                logging.info(f'Copied: {s} to {d}')

def remove_deleted_files(src, dest):
    for item in os.listdir(dest):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if not os.path.exists(s):
            if os.path.isdir(d):
                shutil.rmtree(d)
                logging.info(f'Removed Directory: {d}')
            else:
                os.remove(d)
                logging.info(f'Removed File: {d}')
        elif os.path.isdir(d):
            remove_deleted_files(s, d)

def main():
    parser = argparse.ArgumentParser(description='Sync Directories')
    parser.add_argument('src', type=str, help='Source Path')
    parser.add_argument('dest', type=str, help='Destination Path')
    parser.add_argument('interval', type=int, help='Sync interval in seconds')
    parser.add_argument('log', type=str, help='Log Path')
    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.INFO,
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    while True:
        sync_folders(args.src, args.dest)
        remove_deleted_files(args.src, args.dest)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
