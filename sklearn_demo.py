import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2

from torchvision import transforms, datasets

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def load_celeba():
    '''
    Loads the CelebA dataset from the torchvision module.

    This function applies a transform (resizing imgs to 224x224) for future ML applications and downloads
    the CelebA dataset via a train split to the data folder.
    '''
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
    ])

    datasets.CelebA(root='./data', split='train',
                                        download=True, transform=transform)

def get_dataframes():
    '''
    Loads the identity and attribute data for the CelebA dataset.

    This function reads two files from the CelebA dataset:
    - `identity_CelebA.txt` containing mappings of image IDs to unique identity labels.
    - `list_attr_celeba.txt` containing binary attribute labels (-1 and 1) for each image.

    Returns:
        identity_df (pd.DataFrame): DataFrame with columns `image_id` and `identity_label`, mapping each image ID to a unique identity label.
        attr_df (pd.DataFrame): DataFrame with binary attribute labels for each image, indexed by `image_id`.
    '''
    identity_df = pd.read_csv("./data/celeba/identity_CelebA.txt", delim_whitespace=True, header=None, names=["image_id", "identity_label"])
    
    attr_df = pd.read_csv("./data/celeba/list_attr_celeba.txt", delim_whitespace=True, header=1)
    attr_df.index.name = 'image_id'

    return identity_df, attr_df

def display_imgs(imgs, img=None):
    '''
    Displays a grid of images, including an optional original image followed by a series of similar images.

    This function reads and displays images from specified file paths. If an original image path is provided, 
    it is displayed first, followed by each image in the `imgs` list. All images are converted from BGR to RGB format through OpenCV.

    Args:
        imgs (list of str): List of file paths to images to be displayed as similar images.
        img (str, optional): File path to the original image. If provided, this image is displayed first.
    '''
    imgs = [cv2.imread(f'./data/celeba/img_align_celeba/{image_path}') for image_path in imgs]
    imgs = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB) for image in imgs]

    plt.figure(figsize=(10, 5))

    if img is not None:
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for displaying

        plt.subplot(1, len(imgs) + 1, 1)
        plt.imshow(img)
        plt.title("Original Image")
        plt.axis('off')

    for i, similar_image in enumerate(imgs):
        plt.subplot(1, len(imgs) + 1, i + 2)
        plt.imshow(similar_image)
        plt.title(f"Similar {i + 1}")
        plt.axis('off')

    plt.tight_layout()
    plt.show()

def find_celeb_by_attr(attr_df, identity_df):
    '''
    Filters and displays images of celebrities based on selected attributes, ensuring each image has a unique identity.

    This function allows the user to select attributes by entering attribute numbers, and then filters the dataset (from torchvision) to find celebrities
    matching all selected attributes. The function also limits the result to a specified number of unique identities, displaying each image
    in a grid format.

    Args:
        attr_df (pd.DataFrame): DataFrame containing binary attributes for each image, indexed by `image_id`.
        identity_df (pd.DataFrame): DataFrame containing `image_id` and `identity_label` columns, mapping each image ID to a unique identity label.

    Raises:
        ValueError: If an invalid attribute or non-numeric input for the number of images to display is entered.
    '''
    available_attributes = attr_df.columns.tolist()

    print("Select the attributes by entering their corresponding numbers (separate by commas):")
    
    for i, attr in enumerate(available_attributes, 1):
        print(f"{i}: {attr}")

    selected_nums = input("\nEnter the numbers of the attributes you want (e.g., 1, 3, 5): ").strip().split(',')
    
    # Convert the input into integers and get the corresponding attribute names
    try:
        selected_attrs = [available_attributes[int(num.strip()) - 1] for num in selected_nums]
    except (ValueError, IndexError):
        print("Invalid input. Please select valid numbers.")
        return

    try:
        top_n = int(input("How many similar celebrities do you want to see? ").strip())
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return

    matching_celebs = attr_df.copy()
    for attr in selected_attrs:
        matching_celebs = matching_celebs[matching_celebs[attr] == 1]

    # Merge with identity_df to get identity labels
    matching_celebs = matching_celebs.merge(identity_df, on="image_id")

    # Select unique identities up to the top_n
    unique_matches = []
    seen_identities = set()

    for _, row in matching_celebs.iterrows():
        identity_label = row["identity_label"]
        if identity_label not in seen_identities:
            unique_matches.append(row["image_id"])
            seen_identities.add(identity_label)
        if len(unique_matches) == top_n:
            break

    if len(unique_matches) < top_n:
        print(f"Only found {len(unique_matches)} unique matches. Unable to display {top_n}.")
        return

    display_imgs(imgs=unique_matches)

def find_similar_celebs(attr_df, identity_df, target_image_id, top_n=5):
    '''
    Finds celebrities in the dataset with facial features similar to the target image.

    This function calculates the cosine similarity (through sklearn) between the target image's attributes and all other images in the dataset,
    returning a list of images with unique identities that are most similar to the target.

    Args:
        attr_df (pd.DataFrame): DataFrame containing attributes of images where each row represents an image and each column
            represents a binary attribute (1 or -1).
        identity_df (pd.DataFrame): DataFrame mapping image IDs to unique identity labels. Contains 'image_id' and 'identity_label' columns.
        target_image_id (str): The ID of the target image for similarity comparison.
        top_n (int, optional): The number of most similar unique images to return. Defaults to 5.

    Returns:
        list: A list of image IDs of the most similar images, each with a unique identity.
    '''
    attr_df = attr_df.replace(-1, 0)
    
    target_identity_label = identity_df.loc[identity_df['image_id'] == target_image_id, 'identity_label'].values[0]
    target_attrs = attr_df.loc[target_image_id].values.reshape(1, -1)
    
    similarities = cosine_similarity(target_attrs, attr_df.values)[0]
    
    # Create a DataFrame with image_id, similarity scores, and identity_label
    similarity_df = pd.DataFrame({
        'image_id': attr_df.index,
        'similarity': similarities
    }).merge(identity_df, on='image_id')

    similarity_df = similarity_df[(similarity_df['image_id'] != target_image_id) & 
                                  (similarity_df['identity_label'] != target_identity_label)]

    similarity_df = similarity_df.sort_values(by='similarity', ascending=False)

    unique_similar_celebs = similarity_df.drop_duplicates(subset='identity_label').head(top_n)

    if len(unique_similar_celebs) < top_n:
        print(f"Only found {len(unique_similar_celebs)} unique matches. Unable to display {top_n}.")

    return unique_similar_celebs['image_id'].tolist()

def attr_groupings(attr_df):
    '''
    Clusters images based on attribute similarity and visualizes the clusters with their dominant attributes.

    This function uses K-Means clustering (via sklearn) to group images in the dataset based on their attributes. 
    The function displays the number of items in each cluster, the top three attributes for each cluster, 
    and a PCA-reduced (via sklearn) 2D scatter plot of the clusters.

    Args:
        attr_df (pd.DataFrame): DataFrame containing binary attributes for each image, with attributes as columns and `image_id` as the index.

    Returns:
        pd.DataFrame: The input DataFrame with an additional column `cluster`, indicating the cluster assignment for each image.
    '''
    attr_df = attr_df.replace(-1, 0)

    # Use only the attribute columns
    X = attr_df.values

    # Perform K-Means Clustering
    k = 5
    kmeans = KMeans(n_clusters=k, random_state=42)
    attr_df['cluster'] = kmeans.fit_predict(X)  # Add cluster assignments back to the DataFrame

    print("Number of items in each cluster:")
    print(attr_df['cluster'].value_counts())

    cluster_means = attr_df.groupby('cluster').mean()

    print("\nTop 3 attributes for each cluster:")

    # Loop through each cluster and display the top 3 attributes
    for cluster_num, attributes in cluster_means.iterrows():
        top_attributes = attributes.sort_values(ascending=False).head(3)
        
        print(f"\nCluster {cluster_num} - Top 3 Attributes:")
        for attr, value in top_attributes.items():
            print(f"{attr}: {value:.2f}")

    # Reduce to 2D for visualization using PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=attr_df['cluster'], palette="viridis", s=50)
    plt.title("K-Means Clustering of CelebA Attributes (PCA-reduced)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(title="Cluster")
    plt.show()

    return attr_df
    
def main():
    '''
    Main function to interactively explore the CelebA dataset through various options.

    This function loads the CelebA dataset and presents the user with an interactive menu to:
    - Select specific attributes and display celebrities matching those attributes.
    - Find and display similar celebrities based on facial feature similarity.
    - Cluster celebrities based on attribute similarity and visualize the clusters.
    '''
    load_celeba()

    identity_df, attr_df = get_dataframes()
    print(identity_df)

    while True:
        print("\nSelect an option to display a DataFrame:")
        print("1 - Choose attributes to get a Celebrity of Interest")
        print("2 - Finding Similar Celebrities among the dataset Based on Facial Features")
        print("3 - Exploring Attribute-Based Groupings for the Celebrities")
        print("q - Quit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            find_celeb_by_attr(attr_df, identity_df)
        elif choice == "2":
            while True:
                encoding = input("Enter a number from 000001-202599: ").strip()
                
                # Check if the input is exactly 6 digits and within the range
                if encoding.isdigit() and len(encoding) == 6 and 1 <= int(encoding) <= 202599:
                    break  # Input is valid, so exit the loop
                else:
                    print("Invalid input! Please enter a 6-digit number between 000001 and 202599.")

            n = int(input("How many similar celebrities do you want to see? ").strip())
            
            similar_celebs = find_similar_celebs(attr_df, identity_df, f'{encoding}.jpg', top_n=n)

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