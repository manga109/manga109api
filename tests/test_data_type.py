import manga109api


def test_data_type():
    manga109_root_dir = "tests/data_dummy/"
    p = manga109api.Parser(root_dir=manga109_root_dir)

    for book in p.books:
        annotation = p.get_annotation(book=book, separate_by_tag=False)

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

            assert isinstance(page["contents"], list)
            for obj in page["contents"]:
                if obj["type"] in {"body", "face", "frame", "text"}:
                    assert isinstance(obj["@id"], str)
                    assert isinstance(obj["@xmin"], int)
                    assert isinstance(obj["@xmax"], int)
                    assert isinstance(obj["@ymin"], int)
                    assert isinstance(obj["@ymax"], int)
                    assert isinstance(obj["type"], str)

                    if obj["type"] == "text":
                        assert isinstance(obj["#text"], str)

                # custom tag test
                else:
                    assert isinstance(obj["@id"], str)
                    assert isinstance(obj["@attr_num"], int)
                    assert isinstance(obj["@attr_str"], str)
                    assert isinstance(obj["@attr_mix"], str)
                    assert isinstance(obj["type"], str)

                    for key in (obj.keys() - {"@id", "@attr_num", "@attr_str", "@attr_mix", "type"}):
                        assert isinstance(obj[key], (int, str))

                    if "#text" in obj.keys():
                        assert isinstance(obj["#text"], str)


def test_data_type_separated():
    manga109_root_dir = "tests/data_dummy/"
    p = manga109api.Parser(root_dir=manga109_root_dir)

    for book in p.books:
        annotation = p.get_annotation(book=book, separate_by_tag=True)

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

            for obj_type in page.keys():
                if obj_type in {"body", "face", "frame", "text"}:
                    assert isinstance(page[obj_type], list)
                    for obj in page[obj_type]:
                        assert isinstance(obj["@id"], str)
                        assert isinstance(obj["@xmin"], int)
                        assert isinstance(obj["@xmax"], int)
                        assert isinstance(obj["@ymin"], int)
                        assert isinstance(obj["@ymax"], int)
                        assert obj["type"] == obj_type

                        if obj_type == "text":
                            assert isinstance(obj["#text"], str)

                # custom tag test
                elif obj_type not in {"@index", "@width", "@height"}:
                    for obj in page[obj_type]:
                        assert isinstance(obj["@id"], str)
                        assert isinstance(obj["@attr_num"], int)
                        assert isinstance(obj["@attr_str"], str)
                        assert isinstance(obj["@attr_mix"], str)
                        assert obj["type"] == obj_type
                        
                        for key in (obj.keys() - {"@id", "@attr_num", "@attr_str", "@attr_mix", "type"}):
                            assert isinstance(obj[key], (int, str))
                        
                        if "#text" in obj.keys():
                            assert isinstance(obj["#text"], str)
