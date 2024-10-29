import pytest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for matplotlib

from sklearn_demo import load_celeba, get_dataframes, find_celeb_by_attr, find_similar_celebs, attr_groupings, display_imgs

@pytest.fixture
def mock_data():
    '''
    Fixture to create mock data for testing CelebA-related functions.

    This fixture generates two DataFrames:
    - `identity_df`: Contains a mock mapping of `image_id` to `identity_label`, simulating unique identities for each image.
    - `attr_df`: Contains binary attribute data for each image, with attributes like `Smiling`, `Young`, and `Male`, 
                 simulating the structure of the CelebA attribute dataset.

    Returns:
        identity_df (pd.DataFrame): Mock DataFrame with columns `image_id` and `identity_label`.
        attr_df (pd.DataFrame): Mock DataFrame with binary attributes, indexed by `image_id`.
    '''
    identity_data = {
        'image_id': ['000001.jpg', '000002.jpg', '000003.jpg', '000004.jpg', '000005.jpg'],
        'identity_label': [1, 2, 3, 4, 5]
    }
    identity_df = pd.DataFrame(identity_data)

    attr_data = {
        'image_id': ['000001.jpg', '000002.jpg', '000003.jpg', '000004.jpg', '000005.jpg'],
        'Smiling': [1, -1, 1, -1, 1],
        'Young': [-1, 1, 1, -1, 1],
        'Male': [1, 1, -1, -1, 1]
    }
    attr_df = pd.DataFrame(attr_data).set_index('image_id')

    return identity_df, attr_df

def test_load_celeba(monkeypatch):
    '''
    Tests that the `load_celeba` function properly initializes the CelebA dataset with specified parameters.

    This test replaces `torchvision.datasets.CelebA` with a mock class (`MockCelebA`) to ensure that the 
    `load_celeba` function calls it with the correct arguments without downloading the dataset.

    Args:
        monkeypatch: Pytest fixture for replacing `torchvision.datasets.CelebA` with `MockCelebA`.

    Asserts:
        No exceptions are raised when calling `load_celeba()`.
    '''
    # Define a mock for CelebA with a simple initializer
    class MockCelebA:
        def __init__(self, root, split, download, transform):
            self.root = root
            self.split = split
            self.download = download
            self.transform = transform

    # Replace torchvision.datasets.CelebA with MockCelebA
    monkeypatch.setattr('torchvision.datasets.CelebA', MockCelebA)
    
    # We’re just verifying there’s no error.
    load_celeba()
    
def test_get_dataframes(mock_data, monkeypatch):
    '''
    Tests that `get_dataframes` correctly loads the identity and attribute DataFrames.

    This test mocks `pd.read_csv` to return predefined data (`identity_df` and `attr_df`) 
    instead of reading from files, and checks that `get_dataframes` correctly loads these 
    DataFrames with expected structures.

    Args:
        mock_data (tuple): Fixture providing mock `identity_df` and `attr_df`.
        monkeypatch: Pytest fixture for replacing `pd.read_csv` with the mock function.

    Asserts:
        - The returned objects are DataFrames.
        - `identity_df` contains the columns `image_id` and `identity_label`.
    '''
    identity_df, attr_df = mock_data
    
    # Mock `pd.read_csv` function to return mock data instead of reading from files
    def mock_read_csv(filepath, *args, **kwargs):
        if 'identity_CelebA' in filepath:
            return identity_df
        elif 'list_attr_celeba' in filepath:
            return attr_df
    
    monkeypatch.setattr(pd, 'read_csv', mock_read_csv)
    loaded_identity_df, loaded_attr_df = get_dataframes()

    assert isinstance(loaded_identity_df, pd.DataFrame)
    assert isinstance(loaded_attr_df, pd.DataFrame)
    assert 'image_id' in loaded_identity_df.columns
    assert 'identity_label' in loaded_identity_df.columns

def test_find_celeb_by_attr(mock_data, monkeypatch):
    '''
    Tests that `find_celeb_by_attr` correctly filters and displays images based on selected attributes.

    This test mocks user input for attribute selection and `top_n` to simulate a user selecting 
    attributes and a number of images to display. It also replaces `display_imgs` to validate 
    that each displayed image has a unique identity label.

    Args:
        mock_data (tuple): Fixture providing mock `identity_df` and `attr_df`.
        monkeypatch: Pytest fixture for replacing `input` and `display_imgs`.

    Asserts:
        - The number of images displayed matches the `top_n` input.
        - Each image displayed has a unique `identity_label`.
    '''
    identity_df, attr_df = mock_data

    input_values = iter(["1,3", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))

    def mock_display_imgs(imgs, img=None):
        assert len(imgs) == 2
        unique_labels = identity_df[identity_df['image_id'].isin(imgs)]['identity_label'].nunique()
        assert unique_labels == len(imgs)

    monkeypatch.setattr('sklearn_demo.display_imgs', mock_display_imgs)
    find_celeb_by_attr(attr_df, identity_df)

def test_find_similar_celebs(mock_data):
    '''
    Tests that `find_similar_celebs` returns the correct number of similar images with unique identities.

    This test verifies that `find_similar_celebs` correctly identifies and returns the specified number 
    of similar images for a given target image, ensuring no returned image shares the same identity as 
    the target image.

    Args:
        mock_data (tuple): Fixture providing mock `identity_df` and `attr_df`.

    Asserts:
        - The length of `similar_celebs` matches the specified `top_n`.
        - No image in `similar_celebs` has the same `identity_label` as `target_image_id`.
    '''
    identity_df, attr_df = mock_data
    target_image_id = '000001.jpg'

    similar_celebs = find_similar_celebs(attr_df, identity_df, target_image_id, top_n=3)

    assert len(similar_celebs) == 3

    target_identity = identity_df[identity_df['image_id'] == target_image_id]['identity_label'].values[0]
    assert all(identity_df[identity_df['image_id'] == img]['identity_label'].values[0] != target_identity for img in similar_celebs)

def test_attr_groupings(mock_data, monkeypatch):
    '''
    Tests that `attr_groupings` performs clustering and adds a `cluster` column to `attr_df`.

    This test prevents the PCA plot from displaying and ensures that after calling `attr_groupings`,
    each image is assigned to a cluster by checking for the `cluster` column in the returned DataFrame.

    Args:
        mock_data (tuple): Fixture providing mock `identity_df` and `attr_df`.
        monkeypatch: Pytest fixture for replacing `plt.show`.

    Asserts:
        - `result_df` includes a `cluster` column indicating the cluster assignment for each image.
    '''
    _, attr_df = mock_data

    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)

    result_df = attr_groupings(attr_df)
    assert 'cluster' in result_df.columns

def test_display_imgs(monkeypatch):
    '''
    Tests that `display_imgs` correctly loads and displays images without raising errors.

    This test replaces `cv2.imread` with a dummy image and prevents `plt.show` from displaying the plot,
    verifying that `display_imgs` completes without errors when given valid image paths.

    Args:
        monkeypatch: Pytest fixture for replacing `cv2.imread` and `plt.show`.

    Asserts:
        - No exceptions are raised when calling `display_imgs`.
    '''
    monkeypatch.setattr('cv2.imread', lambda _: np.zeros((224, 224, 3), dtype=np.uint8))
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)
    display_imgs(['000001.jpg', '000002.jpg'], img='000003.jpg')