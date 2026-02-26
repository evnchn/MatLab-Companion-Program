from functions import parse_xml, get_url, get_purpose, get_all_title

FILENAME = 'referencelist_function_cat.xml'
NAMESPACE = {'mw': 'https://www.mathworks.com/help/ref/data'}


def test_parse_xml_returns_tree_and_root():
    tree, root = parse_xml(FILENAME)
    assert tree is not None
    assert root is not None


def test_parse_xml_root_has_children():
    _, root = parse_xml(FILENAME)
    refs = root.findall('.//mw:ref', NAMESPACE)
    assert len(refs) > 0


def test_get_url_returns_string():
    _, root = parse_xml(FILENAME)
    ref = root.findall('.//mw:ref', NAMESPACE)[0]
    url = get_url(ref)
    assert isinstance(url, str)
    assert len(url) > 0


def test_get_purpose_returns_string():
    _, root = parse_xml(FILENAME)
    ref = root.findall('.//mw:ref', NAMESPACE)[0]
    purpose = get_purpose(ref)
    assert isinstance(purpose, str)
    assert len(purpose) > 0


def test_get_all_title_returns_string():
    _, root = parse_xml(FILENAME)
    ref = root.findall('.//mw:ref', NAMESPACE)[0]
    title = get_all_title(ref)
    assert isinstance(title, str)
