import manga109api
import argparse
import os
import glob
from PIL import Image


def args_parser():
    """
    :return: This function returns the manual input of book, annotation_type, and page count.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--book', type=str, help='Name of book to annotate from.')
    parser.add_argument('--annotation', type=str, help='Type of annotation: "body", "face", "frame", "text".')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to annotate.')
    parser.add_argument('--preprocess', action='store_true', help='Preprocess the extracted images to have a uniform size.')
    parser.add_argument('--size', type=int, default=128, help='The uniform size if using preprocessing.')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    ap = args_parser()
    manga109_root_dir = "manga109extracted"
    if not os.path.exists(manga109_root_dir):
        os.makedirs(manga109_root_dir)
    book = ap.book
    page_count = ap.pages
    file_count = [glob.glob(os.path.join(manga109_root_dir, '**', '*.*'), recursive=True)]
    count = len(file_count[0])

    for page_index in range(page_count):
        tracker = 0
        p = manga109api.Parser(root_dir="Manga109s_data")
        annotation = p.get_annotation(book=book)
        img = Image.open(p.img_path(book=book, index=page_index))
        for annotation_type in [ap.annotation]:
            rois = annotation["page"][page_index][annotation_type]
            for roi in rois:
                cropped = img.crop((roi["@xmin"], roi["@ymin"], roi["@xmax"], roi["@ymax"]))
                image_x_dim, image_y_dim = cropped.size
                if ap.preprocess:
                    cropped = cropped.resize((ap.size, ap.size), Image.ANTIALIAS)
                if image_x_dim >= (ap.size / 2) and image_y_dim >= (ap.size / 2):
                    cropped.save("manga109extracted/%s_%d.jpg" % (ap.book, count))
                    count += 1
                    tracker += 1
        print("Extracted %d %s images from page %d of %s's book." % (tracker, ap.annotation, page_index + 1, ap.book))
