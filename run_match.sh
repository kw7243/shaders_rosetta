#!/bin/bash
python match.py --device "cuda:0" --gan_mode "styleganxl" --discr_mode "dino_vits16" --discr_path "/datadrive/shaden/project1/FeatureInversion/pretrained_models/dino_shaders_mixup.pth" --discr_modelname "dinoshadersmixup" --batch_size 16 --epochs 100 --class 0 
