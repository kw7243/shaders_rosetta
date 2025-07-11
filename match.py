import argparse
from transformers import CLIPProcessor, CLIPModel
import torch
import torchvision
from torchvision.models import resnet50
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import clip
from PIL import Image
import requests
import torch.hub
import time
import pickle
import math
import os
from match_utils import matching, stats, nethook, dataset, models

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda:0", type=str)
    parser.add_argument("--save_path", default=None, type=str)
    parser.add_argument("--discr_path", default=None, type=str)  # Optional custom discriminator weights
    parser.add_argument("--gan_mode", required = True, type=str)
    parser.add_argument("--discr_mode", required=True, type=str)
    parser.add_argument("--discr_modelname", required=True, type=str)
    parser.add_argument("--batch_size", default= 10, type=int)
    parser.add_argument("--epochs", default= 100, type=int)
    parser.add_argument("--classidx", default = 0, type=int)
    
    args = parser.parse_args()

    device = torch.device(args.device)
    gan_mode = args.gan_mode
    discr_mode = args.discr_mode
    discr_modelname = args.discr_modelname
    discr_path = args.discr_path
    batch_size = args.batch_size
    epochs = args.epochs

    if gan_mode != "biggan" and gan_mode != "styleganxl":
        classidx = None
    else: 
        classidx = args.classidx

    # Build save_path if not provided
    if args.save_path is None:
        save_path = f"matches/{gan_mode}_{discr_modelname}_cls{classidx}_{batch_size*epochs}"
    else:
        save_path = args.save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    
    
    gan, gan_layers = models.load_gan(gan_mode, device)
    discr, discr_layers = models.load_discr(discr_mode, device, discr_path)

    z_dataset, c_dataset = dataset.create_dataset(gan, gan_mode, batch_size, epochs, classidx, device)

    matching.activ_match_gan(
        gan=gan, gan_layers=gan_layers,
        discr=discr, discr_layers=discr_layers,
        gan_mode=gan_mode,
        discr_mode=discr_mode,
        dataset=(z_dataset, c_dataset),
        epochs=epochs,
        batch_size=batch_size,
        save_path=save_path,
        device=device
    )
    
if __name__ == "__main__":
    main()