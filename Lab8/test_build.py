import json

from build import build

def test_titles_appear_in_output():
    # Make sure we run build in the right directory so data.json is found
    # pytest runs from the root normally, but we configured it to run from Lab8
    build()
    with open("site/index.html") as f:
        html = f.read()
    with open("data.json") as f:
        items = json.load(f)
    for item in items:
        assert item["title"] in html
