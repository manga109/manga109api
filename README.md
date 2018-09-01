# manga109_api

Simple python API to read annotation data of [Manga109](http://www.manga109.org/en/).

Manga109 is the largest dataset for manga (Japanese comic) images,
that is made publicly available for academic research purpose with proper copyright notation.

To download images/annotations of Manga109, please go [here](http://www.manga109.org/en/download) and send the form.
After sending the form, you will receive the password for downloading images (109 titles of manga
as jpeg files)
and annotations (bounding box coordinates of face, body, frame, and speech balloon with texts,
in the form of XML).

This package provides a simple Python API to read annotation data (i.e., parsing XML)
with some utility functions such as reading an image.

## Links
- [Manga109](http://www.manga109.org/en/)
- [Details of annotation data](http://www.manga109.org/en/annotations)
- The original reference paper for Manga109: [[Matsui+, MTAP 2017]](https://link.springer.com/content/pdf/10.1007%2Fs11042-016-4020-z.pdf)
- The paper introducing the annotation data, with the application of object detection (SSD-fork): [[Ogawa+, arXiv 2018]](https://arxiv.org/pdf/1803.08670)

## Installing
You can install the package via pip. The library works with Python 3.5+ on linux
```bash
pip install manga109_api
```

## Example

You can insantiate a parser with the path to the root directory of Manga109.
The annotations are available via the parser.

```python
import manga109_api
from pprint import pprint

manga109_root_dir = "YOUR_DIR/Manga109_2017_09_28"
p = manga109_api.Parser(root_dir=manga109_root_dir)

print(p.books)
# ['ARMS', 'AisazuNihaIrarenai', 'AkkeraKanjinchou', 'Akuhamu', 'AosugiruHaru', ...

pprint(p.annotations["ARMS"])
# {'book': {'@title': 'ARMS',
#           'characters': {'character': [{'@id': '00000003', '@name': '女1'},
#                                        {'@id': '00000010', '@name': '男1'},
#                                        {'@id': '00000090', '@name': 'ロボット1'},
#                                        {'@id': '000000fe', '@name': 'エリー'},
#                                        {'@id': '0000010a', '@name': 'ケイト'},
#                                        {'@id': '0000010e', '@name': '大佐'},
# ...
#           'pages': {'page': [{'@height': 1170, '@index': 0, '@width': 1654},
#                              {'@height': 1170, '@index': 1, '@width': 1654},
#                              {'@height': 1170,
#                               '@index': 2,
#                               '@width': 1654,
#                               'body': {'@character': '00000003',
#                                        '@id': '00000002',
#                                        '@xmax': 548,
#                                        '@xmin': 178,
#                                        '@ymax': 965,
#                                        '@ymin': 660},
#                               'face': {'@character': '00000003',
#                                        '@id': '00000004',
#                                        '@xmax': 456,
#                                        '@xmin': 406,
# ...

pprint(p.annotations["ARMS"]["book"]["pages"]["page"][6])  # annotations of the 7th page
# {'@height': 1170,
#  '@index': 6,
#  '@width': 1654,
#  'body': [{'@character': '00000010',
#            '@id': '00000057',
#            '@xmax': 1155,
#            '@xmin': 1089,
#            '@ymax': 253,
#            '@ymin': 166},
#           {'@character': '00000003',
#            '@id': '0000005f',
#            '@xmax': 302,
#            '@xmin': 125,
#            '@ymax': 451,
#            '@ymin': 314},
# ... 

print(p.img_path(book="ARMS", index=6))  # image path to the 7th page
# YOUR_DIR/Manga109_2017_09_28/images/ARMS/006.jpg

```

An example of visualization is as follows.
```python
import matplotlib as plt

```


## Author
- [Yusuke Matsui](http://yusukematsui.me/)

## Citation
When you make use of images in Manga109, please cite the following paper:

    @article{mtap_matsui_2017,
        author={Yusuke Matsui and Kota Ito and Yuji Aramaki and Azuma Fujimoto and Toru Ogawa and Toshihiko Yamasaki and Kiyoharu Aizawa},
        title={Sketch-based Manga Retrieval using Manga109 Dataset},
        journal={Multimedia Tools and Applications},
        volume={76},
        number={20},
        pages={21811--21838},
        year={2017}
    }

When you use annotation data of Manga109, please cite this:

    @article{corr_ogawa_2018,
        author={Toru Ogawa and Atsushi Otsubo and Rei Narita and Yusuke Matsui and Toshihiko Yamasaki and Kiyoharu Aizawa},
        title={Object Detection for Comics using Manga109 Annotations},
        journal={CoRR},
        volume={abs/1803.08670},
        year={2018}
    }
