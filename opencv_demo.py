'''
For those with Nvidia Graphics Cards ->

(Ensure that you have the necessary CUDA12.1 Drivers downloaded and set in your PATH variable)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

(You may run into an issue with torchvision. In this case, just run the following to force uninstall and reinstall)
pip3 uninstall torchvision
pip3 install torchvision --extra-index-url https://download.pytorch.org/whl/cu121

(Run this in the command line to ensure that you have CUDA12.1)
nvcc --version
'''

import torch
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets

# The OpenCV library
import cv2

def cuda_device():
    if torch.cuda.is_available():
        print(torch.cuda.get_device_name())
        device = torch.device("cuda")
    else:
        print("cpu")
        device = torch.device("cpu")

    return device

def load_celeba():
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
    ])

    celeba = torchvision.datasets.CelebA(root='./celeba_data', split='train',
                                        download=True, transform=transform)

def load_cifar100():
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
    ])

    cifar100 = datasets.CIFAR100(root='./data', train=True, download=True, transform=transform)

def main():
    device = cuda_device()

    load_celeba()
    load_cifar100()

    print(f"Device: {device}")

if __name__ == "__main__":
    main()