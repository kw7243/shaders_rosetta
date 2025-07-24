#!/bin/bash
python match.py --device "cuda:2" --gan_mode "styleganxl" --discr_mode "dino_vits16" --discr_path "/datadrive/shaden/project1/FeatureInversion/pretrained_models/dino_shaders_kml.pth" --discr_modelname "dinoshaderskml" --batch_size 16 --epochs 100 --class 0 > log.txt 2>&1
