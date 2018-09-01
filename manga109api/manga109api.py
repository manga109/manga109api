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
        self.annotations = {}  # annotation in the form of dict

        with (self.root_dir / "books.txt").open("rt") as f:
            self.books = [line.rstrip() for line in f]

        for book in self.books:
            if book_titles != "all" and book not in book_titles:
                continue
            with (self.root_dir / "annotations" / (book + ".xml")).open("rt") as f:
                annotation = xmltodict.parse(f.read())
            annotation = json.loads(json.dumps(annotation))  # OrderedDict -> dict
            _convert_str_to_int_recursively(annotation)  # str -> int, for some attributes
            self.annotations[book] = annotation

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