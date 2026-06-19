import json

import os
from build import build

def test_titles_appear_in_output():
    build()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "site", "index.html")) as f:
        html = f.read()
    with open(os.path.join(base_dir, "data.json")) as f:
        items = json.load(f)
    for item in items:
        assert item["title"] in html
