import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from torchvision import transforms, datasets

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import cv2

def load_celeba():
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
    ])

    datasets.CelebA(root='./data', split='train',
                                        download=True, transform=transform)

def get_dataframes():
    identity_df = pd.read_csv("./data/celeba/identity_CelebA.txt", delim_whitespace=True, header=None, names=["image_id", "encoding"])
    
    attr_df = pd.read_csv("./data/celeba/list_attr_celeba.txt", delim_whitespace=True, header=1)
    attr_df.index.name = 'image_id'

    return identity_df, attr_df

def display_imgs(imgs, img=None):
    # Load similar images
    imgs = [cv2.imread(f'./data/celeba/img_align_celeba/{image_path}') for image_path in imgs]
    imgs = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB) for image in imgs]  # Convert to RGB

    # Display the images in a grid
    plt.figure(figsize=(10, 5))

    # Load the original image
    if img is not None:
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for displaying

        # Display the original image
        plt.subplot(1, len(imgs) + 1, 1)  # 1 row, (number of similar images + 1) columns
        plt.imshow(img)
        plt.title("Original Image")
        plt.axis('off')

    # Display the similar images
    for i, similar_image in enumerate(imgs):
        plt.subplot(1, len(imgs) + 1, i + 2)  # Move to the next subplot
        plt.imshow(similar_image)
        plt.title(f"Similar {i + 1}")
        plt.axis('off')

    plt.tight_layout()
    plt.show()

def find_similar_celebs(attr_df, target_image_id, top_n=5):
    '''
    Finding Similar Celebrities among the dataset Based on Facial Features
    '''
    attr_df = attr_df.replace(-1, 0)

    target_attrs = attr_df.loc[target_image_id].values.reshape(1, -1)
    
    # Calculate cosine similarity between the target and all other celebrities
    similarities = cosine_similarity(target_attrs, attr_df.values)[0]
    
    # Sort the similarities and get the top N most similar celebrities
    most_similar = np.argsort(similarities)[::-1][1:top_n+1]  # Skipping self-comparison
    
    similar_celebs = attr_df.iloc[most_similar].index.tolist()
    
    return similar_celebs

def find_celeb_by_attr(attr_df):
    # Available attributes from CelebA
    available_attributes = attr_df.columns.tolist()

    # Display available attributes for the user to choose from
    print("Select the attributes by entering their corresponding numbers (separate by commas):")
    
    # Display the list of attributes with index numbers
    for i, attr in enumerate(available_attributes, 1):
        print(f"{i}: {attr}")

    # Get user input for attribute selection
    selected_nums = input("\nEnter the numbers of the attributes you want (e.g., 1, 3, 5): ").strip().split(',')
    
    # Convert the input into integers and get the corresponding attribute names
    try:
        selected_attrs = [available_attributes[int(num.strip()) - 1] for num in selected_nums]
    except (ValueError, IndexError):
        print("Invalid input. Please select valid numbers.")
        return

    # Get user input for how many celebrities to display
    try:
        top_n = int(input("How many similar celebrities do you want to see? ").strip())
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return

    # Filter the celebrities that match all selected attributes
    matching_celebs = attr_df.copy()
    for attr in selected_attrs:
        matching_celebs = matching_celebs[matching_celebs[attr] == 1]

    # Return top N matches
    matching_celebs = matching_celebs.index[:top_n].tolist()

    display_imgs(imgs=matching_celebs)

def attr_groupings(attr_df):
    # Convert (-1, 1) to (0, 1) for binary representation
    attr_df = attr_df.replace(-1, 0)

    # Use only the attribute columns (drop the index for clustering)
    X = attr_df.values  # This will exclude the image_id index automatically

    # Perform K-Means Clustering
    k = 5  # Define the number of clusters
    kmeans = KMeans(n_clusters=k, random_state=42)
    attr_df['cluster'] = kmeans.fit_predict(X)  # Add cluster assignments back to the DataFrame

    # Show the number of items in each cluster
    print("Number of items in each cluster:")
    print(attr_df['cluster'].value_counts())

    # Calculate mean attributes for each cluster
    cluster_means = attr_df.groupby('cluster').mean()

    print("\nTop 3 attributes for each cluster:")

    # Loop through each cluster and display the top 3 attributes
    for cluster_num, attributes in cluster_means.iterrows():
        # Sort attributes in descending order and select the top 3
        top_attributes = attributes.sort_values(ascending=False).head(3)
        
        print(f"\nCluster {cluster_num} - Top 3 Attributes:")
        for attr, value in top_attributes.items():
            print(f"{attr}: {value:.2f}")

    # Reduce to 2D for visualization using PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # Plot the clusters
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=attr_df['cluster'], palette="viridis", s=50)
    plt.title("K-Means Clustering of CelebA Attributes (PCA-reduced)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(title="Cluster")
    plt.show()
    
def main():
    load_celeba()

    identity_df, attr_df = get_dataframes()

    while True:
        print("\nSelect an option to display a DataFrame:")
        print("1 - Choose attributes to get a Celebrity of Interest")
        print("2 - Finding Similar Celebrities among the dataset Based on Facial Features")
        print("3 - Exploring Attribute-Based Groupings for the Celebrities")
        print("q - Quit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            find_celeb_by_attr(attr_df)
        elif choice == "2":
            while True:
                encoding = input("Enter a number from 000001-202599: ").strip()
                
                # Check if the input is exactly 6 digits and within the range
                if encoding.isdigit() and len(encoding) == 6 and 1 <= int(encoding) <= 202599:
                    break  # Input is valid, so exit the loop
                else:
                    print("Invalid input! Please enter a 6-digit number between 000001 and 202599.")

            n = int(input("How many similar celebrities do you want to see? ").strip())
            
            similar_celebs = find_similar_celebs(attr_df, f'{encoding}.jpg', top_n=n)

            display_imgs(similar_celebs, img=f'./data/celeba/img_align_celeba/{encoding}.jpg')
        elif choice == "3":
            attr_groupings(attr_df)
        elif choice == "q":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
        
if __name__ == "__main__":
    main()