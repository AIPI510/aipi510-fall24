import pandas as pd

# The PyTorch Module
import torch
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

    celeba_data = datasets.CelebA(root='./data', split='train',
                                        download=True, transform=transform)
    
    return celeba_data

def get_dataframes():
    identity_df = pd.read_csv("./data/celeba/identity_CelebA.txt", delim_whitespace=True, header=None, names=["image_id", "encoding"])
    
    attr_df = pd.read_csv("./data/celeba/list_attr_celeba.txt", delim_whitespace=True, header=1)
    attr_df.index.name = 'image_id'

    bbox_df = pd.read_csv("./data/celeba/list_bbox_celeba.txt", delim_whitespace=True, header=1)
    
    partition_df = pd.read_csv("./data/celeba/list_eval_partition.txt", delim_whitespace=True, header=None, names=["image_id", "partition"])

    landmarks_df = pd.read_csv("./data/celeba/list_landmarks_align_celeba.txt", delim_whitespace=True, header=1)

    return identity_df, attr_df, bbox_df, partition_df, landmarks_df

def main():
    device = cuda_device()

    # celeba_data = load_celeba()

    identity_df, attr_df, bbox_df, partition_df, landmarks_df = get_dataframes()

    # Menu
    def show_menu():
        print("\nSelect an option to display a DataFrame:")
        print("1 - Identity DataFrame")
        print("2 - Attributes DataFrame")
        print("3 - Bounding Boxes DataFrame")
        print("4 - Partition DataFrame")
        print("5 - Landmarks DataFrame")
        print("q - Quit")

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            print(identity_df.head())
        elif choice == "2":
            print(attr_df.head())
        elif choice == "3":
            print(bbox_df.head())
        elif choice == "4":
            print(partition_df.head())
        elif choice == "5":
            print(landmarks_df.head())
        elif choice == "q":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
        
if __name__ == "__main__":
    main()