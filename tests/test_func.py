import manga109api
from pathlib import Path


def test_img_path():
    manga109_root_dir = "tests/data_dummy/"
    p = manga109api.Parser(root_dir=manga109_root_dir)

    img1 = Path(p.img_path(book="TitleA", index=0)).absolute()
    img2 = Path("tests/data_dummy/images/TitleA/000.jpg").absolute()
    assert(img1 == img2)


def test_format_annotation():
    annotation = {
        'book': {
            '@title': 'AAA',
            'characters': {'character': [
                {'id': '123', 'name': 'yyy'}
            ]},
            'pages': {'page': [
                {'index': 234, 'width': 345, 'height': 456,
                 'frame': [{'id': '567', 'xmin': 11, 'ymin': 22, 'xmax': 33, 'ymax': 44}]}
            ]}
        }
    }
    gt = {
        'title': 'AAA',
        'character': [{'id': '123', 'name': 'yyy'}],
        'page': [
            {'index': 234, 'width': 345, 'height': 456, 'face': [], 'body': [], 'text': [],
             'frame': [{'id': '567', 'xmin': 11, 'ymin': 22, 'xmax': 33, 'ymax': 44}]}
        ]
    }

    ret = manga109api.manga109api._format_annotation(annotation)
    assert(gt == ret)

def test_format_page_dict_style():
    page = [{'body': [123], 'face': 123, 'frame': []}]
    gt = [{'body': [123], 'face': [123], 'frame': [], 'text': []}]
    manga109api.manga109api._format_page_dict_style(page)
    assert(gt == page)

def test_convert_str_to_int_recursively():
    annotation = [{'@xmax': '234', 'id': '0007a8be'}]
    gt = [{'@xmax': 234, 'id': '0007a8be'}]
    manga109api.manga109api._convert_str_to_int_recursively(annotation)
    assert(gt == annotation)
