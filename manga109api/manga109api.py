import pathlib
import json
import xmltodict


class Parser(object):
    def __init__(self, root_dir):
        """
        Manga109 annotation parser

        Args:
            root_dir (str): The path of the root directory of Manga109 data, e.g., 'YOUR_PATH/Manga109_2017_09_28'
        """
        self.root_dir = pathlib.Path(root_dir)
        self.books = []  # book titles

        with (self.root_dir / "books.txt").open("rt", encoding='utf-8') as f:
            self.books = [line.rstrip() for line in f]

    def get_annotation(self, book, annotation_type="annotations"):
        """
        Given a book title, return annotation in the form of dict.

        Args:
            book (str): A title of a book. Should be in self.books.

        Returns:
            annotation (dict): Annotation data consists of dict.
        """
        assert book in self.books
        with (self.root_dir / annotation_type / (book + ".xml")).open("rt", encoding= 'utf-8') as f:
            annotation = xmltodict.parse(f.read())
        annotation = json.loads(json.dumps(annotation))  # OrderedDict -> dict
        annotation = _format_annotation(annotation)
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
    Given annotation data, convert to an easily accessible dict.
    For example, dict['book']['characters']['character'] -> dict['character']

    Args:
        annotation (dict): Annotation data. Root key is 'book'.

    Returns:
        annotation (dict): Annotation data. Root keys are 'title', 'character' and 'page'.
    """

    title = annotation['book']['@title']
    try:
        character = annotation['book']['characters']['character']
    except:
        character = None
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
    Format page annotation data. Make page data have the same key, and align the style of dict.
    For example,
      in:  [{'body': [123], 'face': 123, 'frame': []}]
      out: [{'body': [123], 'face': [123], 'frame': [], 'text': []}]

    Args:
        page (dict): Annotation data for all pages including info such as frame, text, etc.
    """
    types = ['body', 'face', 'frame', 'text']
    for i, p in enumerate(page):
        for t in set(types) - set(p.keys()):
            page[i][t] = []
        for t in types:
            if not isinstance(p[t], list):
                page[i][t] = [page[i][t]]


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
