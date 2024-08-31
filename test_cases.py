import pathlib
import filecmp

from hugging_face_api import main


def test_main(tmp_path: pathlib.Path, datadir: pathlib.Path):
    expected_train_csv_file = datadir / "train.csv"
    expected_test_csv_file = datadir / "test.csv"

    real_train_csv_file = tmp_path / "train.csv"
    real_test_csv_file = tmp_path / "test.csv"

    main(real_train_csv_file, real_test_csv_file)

    assert filecmp.cmp(expected_train_csv_file, real_train_csv_file)
    assert filecmp.cmp(expected_test_csv_file, real_test_csv_file)
