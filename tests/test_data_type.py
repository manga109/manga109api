import manga109api


def test_data_type():
    manga109_root_dir = "tests/data_dummy/"
    p = manga109api.Parser(root_dir=manga109_root_dir)

    for book in p.books:
        annotation = p.get_annotation(book=book)

        # title
        assert isinstance(annotation["title"], str)

        # character
        assert isinstance(annotation["character"], list)
        for character in annotation["character"]:
            assert isinstance(character["@id"], str)
            assert isinstance(character["@name"], str)

        # page
        assert isinstance(annotation["page"], list)
        for page in annotation["page"]:
            assert isinstance(page["@index"], int)
            assert isinstance(page["@width"], int)
            assert isinstance(page["@height"], int)
            
            for obj_type in {"body", "face", "frame", "text"}:
                assert isinstance(page[obj_type], list)
                for obj in page[obj_type]:
                    assert isinstance(obj["@id"], str)
                    assert isinstance(obj["@xmin"], int)
                    assert isinstance(obj["@xmax"], int)
                    assert isinstance(obj["@ymin"], int)
                    assert isinstance(obj["@ymax"], int)

                    if obj_type == "text":
                        assert isinstance(obj["#text"], str)
