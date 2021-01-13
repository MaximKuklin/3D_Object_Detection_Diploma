from argparse import ArgumentParser
from tqdm import tqdm

import os
import requests
import os.path as osp
import numpy as np

ANNO_DIR = 'annotations'
VIDEO_DIR = 'videos'
CLASSES = ['bike', 'book', 'bottle', 'camera', 'cereal_box',	'chair', 'cup', 'laptop', 'shoe']


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--save_path', type=str)
    parser.add_argument('--classes', choices=CLASSES, type=str)
    args = parser.parse_args()
    return args


def create_filename(video_filename):
    video_filename = video_filename.rsplit('/')
    # name = '_'.join([video_filename[-3], video_filename[-2]])+'.MOV'
    # name = osp.join(video_filename[-4], name)
    name = '_'.join([video_filename[-4], video_filename[-3], video_filename[-2], video_filename[-1]])
    return name

def download_data(args):
    save_path = args.save_path
    classes = args.classes

    if not osp.exists(save_path):
        os.makedirs(save_path)

    public_url = "https://storage.googleapis.com/objectron"
    blob_path = public_url + "/v1/index/cup_annotations_test"
    video_ids = requests.get(blob_path).text
    video_ids = video_ids.split('\n')
    # Download the first ten videos in cup test dataset
    for i in tqdm(range(20)):
        video_filename = public_url + "/videos/" + video_ids[i] + "/video.MOV"
        metadata_filename = public_url + "/videos/" + video_ids[i] + "/geometry.pbdata"
        annotation_filename = public_url + "/annotations/" + video_ids[i] + ".pbdata"
        video_save_filename = osp.join(save_path, create_filename(video_filename))
        # video.content contains the video file.
        video = requests.get(video_filename)
        # metadata = requests.get(metadata_filename)
        # annotation = requests.get(annotation_filename)
        file = open(video_save_filename, "wb")
        file.write(video.content)
        file.close()


if __name__ == '__main__':
    args = parse_args()
    download_data(args)
