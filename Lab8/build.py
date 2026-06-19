import json
import os

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "data.json")) as f:
        items = json.load(f)
        
    lines = []
    lines.append("<html><body>")
    lines.append("<h1>My list</h1>")
    lines.append("<ul>")
    
    for item in items:
        lines.append(f"  <li><strong>{item['title']}</strong>: {item['description']}</li>")
        
    lines.append("</ul>")
    lines.append("</body></html>")
    
    os.makedirs(os.path.join(base_dir, "site"), exist_ok=True)
    with open(os.path.join(base_dir, "site", "index.html"), "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    build()
