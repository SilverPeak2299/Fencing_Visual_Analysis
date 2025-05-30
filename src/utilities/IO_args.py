import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Return file path')
    parser.add_argument('file_path', type=str, help='Path to the file')
    args = parser.parse_args()
    return args.file_path