import manga109api
from pathlib import Path


def test_img_path():
    manga109_root_dir = "tests/data_dummy/"
    p = manga109api.Parser(root_dir=manga109_root_dir)

    img1 = Path(p.img_path(book="TitleA", index=0)).absolute()
    img2 = Path("tests/data_dummy/images/TitleA/000.jpg").absolute()
    assert(img1 == img2)
