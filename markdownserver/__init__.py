#!/usr/bin/python

from os import getcwd, listdir
from flask import Flask, Response
from os.path import isfile, join, splitext

from markdown import markdown

app = Flask(__name__)


def list_dir():
    output = ""
    for file_name in listdir(getcwd()):
        file_path = join(getcwd(), file_name)
        if not isfile(file_path): continue

        output += f"<a href=\"{file_name}\">{file_name}</a>"

    return output

def get_file(file_path):
    with open(file_path) as f: return f.read()


template = """
<link rel="stylesheet" href="assets/css/markdown.css">
<link rel="stylesheet" href="assets/css/{1}.css">

<body>
  <div class="markdown {1}">
    {0}
  </div>
</body>
"""

@app.route('/assets/css/<resource>')
def assets_css(resource): 
    complete_path = join(getcwd(), f"assets/css/{resource}")
    return get_file(complete_path)

@app.route('/', defaults={'path': '/'})
@app.route('/<path>')
def resource(path): 
    if path == "/": return list_dir()

    complete_path = join(getcwd(), path)

    try:
        content = get_file(complete_path)
        html = markdown(content, 
                        extensions=['fenced_code'])

        themes = [  "clearness",
                    "clearness-dark",
                    "github",
                    "haroopad",
                    "metro-vibes",
                    "metro-vibes-dark",
                    "node-dark",
                    "solarized-dark",
                    "solarized-light",
                    "wood",
                    "wood-ri"]

        return Response(template.format(html, themes[6]))

    except Exception as e:
        return Response(f"{e}")

def main():
    app.run(host='0.0.0.0', 
            port=8000)

if __name__ == '__main__':
    main()
