""" 
I extracted this python script from the https://github.com/ultralytics/ultralytics/blob/main/ultralytics/datasets/Objects365.yaml page. 
However, I re-wrote the directory aspect of the code to eliminate yaml, and directory issues. 
I made this extraction so I could download the object365 dataset to any local machine 
I want without running the yolov8 train script for object365. """


#run pip install ultralytics to the local machine before running
from tqdm import tqdm

from ultralytics.yolo.utils.checks import check_requirements
from ultralytics.yolo.utils.downloads import download
from ultralytics.yolo.utils.ops import xyxy2xywhn

import numpy as np
import yaml 
import pathlib 
import os

check_requirements('pycocotools>=2.0')
from pycocotools.coco import COCO

# Make Directories
dir = 'Datasets'
for p in 'images', 'labels':
    if not os.path.exists(dir + '/' + p):
        os.mkdir(dir + '/' + p)
    else:
        os.path.join(dir, p)

    for q in 'train', 'val':
        if not os.path.exists(dir + '/' + q):
            os.mkdir(dir + '/' + q)
        else:
            os.path.join(dir, q)
        
  # Train, Val Splits
for split, patches in [('train', 50 + 1), ('val', 43 + 1)]:
    print(f"Processing {split} in {patches} patches ...")
    images, labels = os.path.join(dir, 'images', split), os.path.join(dir, 'labels', split)
    # Download
    url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/{split}/"
    if split == 'train':
        download([f'{url}zhiyuan_objv2_{split}.tar.gz'], dir=dir, delete=False)  # annotations json
        download([f'{url}patch{i}.tar.gz' for i in range(patches)], dir=images, curl=True, delete=False, threads=8)
    elif split == 'val':
        download([f'{url}zhiyuan_objv2_{split}.json'], dir=dir, delete=False)  # annotations json
        download([f'{url}images/v1/patch{i}.tar.gz' for i in range(15 + 1)], dir=images, curl=True, delete=False, threads=8)
        download([f'{url}images/v2/patch{i}.tar.gz' for i in range(16, patches)], dir=images, curl=True, delete=False, threads=8)
      # Move
    for f in tqdm(images.rglob('*.jpg'), desc=f'Moving {split} images'):
        f.rename(images / f.name)  # move to /images/{split}
      # Labels
      
    coco = COCO(dir / f'zhiyuan_objv2_{split}.json')
    names = [x["name"] for x in coco.loadCats(coco.getCatIds())]
    for cid, cat in enumerate(names):
        catIds = coco.getCatIds(catNms=[cat])
        imgIds = coco.getImgIds(catIds=catIds)
        for im in tqdm(coco.loadImgs(imgIds), desc=f'Class {cid + 1}/{len(names)} {cat}'):
            width, height = im["width"], im["height"]
            path = Path(im["file_name"])  # image filename
            try:
                with open(labels / path.with_suffix('.txt').name, 'a') as file:
                    annIds = coco.getAnnIds(imgIds=im["id"], catIds=catIds, iscrowd=None)
                    for a in coco.loadAnns(annIds):
                        x, y, w, h = a['bbox']  # bounding box in xywh (xy top-left corner)
                        xyxy = np.array([x, y, x + w, y + h])[None]  # pixels(1,4)
                        x, y, w, h = xyxy2xywhn(xyxy, w=width, h=height, clip=True)[0]  # normalized and clipped
                        file.write(f"{cid} {x:.5f} {y:.5f} {w:.5f} {h:.5f}\n")
            except Exception as e:
                  print(e)
