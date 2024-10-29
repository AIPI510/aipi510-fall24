import pytest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for matplotlib
from sklearn_demo import load_celeba, get_dataframes, find_celeb_by_attr, find_similar_celebs, attr_groupings, display_imgs

@pytest.fixture
def mock_data():
    # Mock identity_df and attr_df data
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
    # Define a mock for CelebA with a simple initializer
    class MockCelebA:
        def __init__(self, root, split, download, transform):
            self.root = root
            self.split = split
            self.download = download
            self.transform = transform

    # Replace torchvision.datasets.CelebA with MockCelebA
    monkeypatch.setattr('torchvision.datasets.CelebA', MockCelebA)
    
    # Call load_celeba and verify that it instantiates CelebA with expected arguments
    load_celeba()
    # Since MockCelebA does not return anything, we’re just verifying there’s no error.

def test_get_dataframes(mock_data, monkeypatch):
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
    identity_df, attr_df = mock_data

    # Mock user input for selecting attributes and top_n
    input_values = iter(["1,3", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))

    # Instead of checking display, we’ll check if the output has unique identity labels
    def mock_display_imgs(imgs, img=None):
        assert len(imgs) == 2  # Expect 2 unique images based on user input
        unique_labels = identity_df[identity_df['image_id'].isin(imgs)]['identity_label'].nunique()
        assert unique_labels == len(imgs)  # Ensure each image has a unique identity

    monkeypatch.setattr('sklearn_demo.display_imgs', mock_display_imgs)
    find_celeb_by_attr(attr_df, identity_df)

def test_find_similar_celebs(mock_data):
    identity_df, attr_df = mock_data
    target_image_id = '000001.jpg'

    similar_celebs = find_similar_celebs(attr_df, identity_df, target_image_id, top_n=3)

    # Check if similar_celebs has the right number of results
    assert len(similar_celebs) == 3
    # Ensure no image in similar_celebs has the same identity as target_image_id
    target_identity = identity_df[identity_df['image_id'] == target_image_id]['identity_label'].values[0]
    assert all(identity_df[identity_df['image_id'] == img]['identity_label'].values[0] != target_identity for img in similar_celebs)

def test_attr_groupings(mock_data, monkeypatch):
    _, attr_df = mock_data

    # Prevent display
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)

    # Capture returned DataFrame and verify the cluster column
    result_df = attr_groupings(attr_df)
    assert 'cluster' in result_df.columns

def test_display_imgs(monkeypatch):
    monkeypatch.setattr('cv2.imread', lambda _: np.zeros((224, 224, 3), dtype=np.uint8))
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: None)
    display_imgs(['000001.jpg', '000002.jpg'], img='000003.jpg')