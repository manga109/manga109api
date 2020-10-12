import pathlib
import xml.etree.ElementTree as ET


class Parser(object):
    annotation_tags = ["frame", "face", "body", "text"]

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

    def get_annotation(self, book, annotation_type="annotations", separate_by_tag=True):
        """
        Given a book title, return its annotations as a dict.

        Args:
            book (str): The title of the book to get the annotations of.
                The title must be contained in the list `self.books`.
            annotation_type (str) default `"annotations"` : The directory to load the xml data from.
            separate_by_tag (bool) default `True` : When set to `True`, each annotation data type
                ("frame", "face", "body", "text") will be stored in a different list in the output
                dictionary. When set to `False`, all of the annotation data will be stored in a
                single list in the output dictionary. In the latter case, the data in the list will
                appear in the same order as in the original XML file.

        Returns:
            annotation (dict): The annotation data
        """
        assert book in self.books

        def int_literals_to_int(t):
            """
            Convert integer literal strings to integers,
            if the stringified result of the integer expression
            matches the original string.
            The following keys will be affected with this function:
            '@index', '@width', '@height', '@xmax', '@ymax', '@xmin', '@ymin'
            """
            try:
                if str(t) == str(int(t)):
                    return int(t)          # Example case: t == "42"
                else:
                    return t               # Example case: t == "00001234"
            except ValueError as e:
                return t                   # Example case: t == "some text" or t == "000012ab"

        def formatted_dict(d):
            """
            - Prepends an "@" in front of each key of a given dict.
            - Also applies `int_literals_to_int` to each value of the given dict.
            Example:
                input:  {"index": "5", "title": "a"}
                output: {"@index": 5,  "@title": "a"}
            """
            return dict([("@" + k, int_literals_to_int(v)) for k, v in d.items()])

        with (self.root_dir / annotation_type / (book + ".xml")).open("rt", encoding='utf-8') as f:
            xml = ET.parse(f).getroot()
        annotation = {"title": xml.attrib["title"]}

        characters = []
        try:
            for t in xml.find("characters"):
                characters.append(formatted_dict(t.attrib))
        except:
            pass
        annotation["character"] = characters

        pages = []
        for page_xml in xml.find("pages"):
            page = formatted_dict(page_xml.attrib)

            if separate_by_tag:
                for annotation_tag in self.annotation_tags:
                    page[annotation_tag] = []
            else:
                page["contents"] = []

            for bb_xml in page_xml:
                d = formatted_dict(bb_xml.attrib)
                if bb_xml.text is not None:
                    d["#text"] = bb_xml.text
                d["type"] = bb_xml.tag

                if separate_by_tag:
                    try:
                        page[bb_xml.tag].append(d)
                    except:
                        page[bb_xml.tag] = [d]
                else:
                    page["contents"].append(d)

            pages.append(page)
        annotation["page"] = pages
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
