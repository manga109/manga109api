import pathlib
import json
import xmltodict


class Parser(object):
    def __init__(self, root_dir, book_titles="all"):
        """
        Manga109 annotation parser

        Args:
            root_dir (str): The path of the root directory of Manga109 data, e.g., 'YOUR_PATH/Manga109_2017_09_28'
            book_titles (str or list): The book titles to be parsed.
                For example, if book_titles = ["ARMS", "AisazuNihaIrarenai"], these two books are read.
                The default value is "all", where all books are read
        """
        self.root_dir = pathlib.Path(root_dir)
        self.books = []  # book titles

        with (self.root_dir / "books.txt").open("rt", encoding='utf-8') as f:
            self.books = [line.rstrip() for line in f]

    def get_annotation(self, book):
        """
        タイトルを引数にアノテーションを返す

        Args:
            book (str): 漫画のタイトル

        Returns:
            dict: 漫画のアノテーション 
        """
        with (self.root_dir / "annotations" / (book + ".xml")).open("rt", encoding='utf-8') as f:
            annotation = xmltodict.parse(f.read())
        annotation = json.loads(json.dumps(annotation))  # OrderedDict -> dict
        annotation = _format_annotation(annotation)  # アノテーションの整形
        _convert_str_to_int_recursively(annotation)  # str -> int, for some attributes
        return annotation

    def img_path(self, book, index):
        """
        Given a book title and an index of a page, return the correct image path

        Args:
            book (str): A title of a book. Should be in self.books.
            index (int): An index of a page

        Returns:
            str: A path to the selected image
        """
        assert book in self.books
        assert isinstance(index, int)
        return str((self.root_dir / "images" / book / (str(index).zfill(3) + ".jpg")).resolve())


def _format_annotation(annotation):
    """
    複雑な階層構造をシンプルにする処理
    """

    title = annotation['book']['@title']
    character = annotation['book']['characters']['character']
    page = annotation['book']['pages']['page']

    if not isinstance(character, list):
        character = [character]
    if not isinstance(page, list):
        page = [page]
    _format_page_dict_style(page)

    return {
        'title': title,
        'character': character,
        'page': page
    }


def _format_page_dict_style(page):
    """
    各ページのアノテーションについて、存在しないキーを補いbody・face・frame・textをlist型に揃える
    """
    required_keys = {'@index', '@width', '@height', 'body', 'face', 'frame', 'text'}
    for i, p in enumerate(page):
        for k in required_keys - set(p.keys()):  # FIXME: 存在しないキーを補う処理だが必要ないかも（index, width, heightはリスト型で合ってるのか？）
            page[i][k] = []
        for k in ['body', 'face', 'frame', 'text']:
            if not isinstance(p[k], list):
                page[i][k] = [page[i][k]]


def _convert_str_to_int_recursively(annotation):
    """
    Given annotation data (nested list or dict), convert some attributes from string to integer.
    For example, [{'@xmax': '234', 'id': '0007a8be'}] -> [{'@xmax': 234, 'id': '0007a8be'}]

    Args:
        annotation  (list or dict): Annotation date that consists of list or dict. Can be deeply nested.
    """
    if isinstance(annotation, dict):
        for k, v in annotation.items():
            if k in ['@index', '@width', '@height', '@xmax', '@ymax', '@xmin', '@ymin']:
                annotation[k] = int(v)
            _convert_str_to_int_recursively(v)
    elif isinstance(annotation, list):
        for v in annotation:
            _convert_str_to_int_recursively(v)
