#!/usr/bin/python

from os import getcwd, listdir
from flask import Flask, Response
from os.path import isfile, join, splitext

from markdown import markdown, Markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

app = Flask(__name__)


def list_dir():
    output = ""
    for file_name in listdir(getcwd()):
        file_path = join(getcwd(), file_name)
        if not isfile(file_path): continue

        output += f"<a href=\"{file_name}\">{file_name}</a>"

    return output

def get_file(file_path):
    with open(file_path, 'rb') as f: 
        content = f.read()
        content = content.decode("utf-8")
        return content

def markdown_to_html(markdown_text):
    # html = markdown(markdown_text, 
                    # extensions=[    'codehilite',
                                    # GithubFlavoredMarkdownExtension()])

    # Factory-like:
    md = Markdown(extensions=[  'codehilite',
                                'markdown.extensions.fenced_code',
                                GithubFlavoredMarkdownExtension() ])
    html = md.convert(markdown_text)
    return html

import subprocess
def markdown_file_to_html(markdown_file):
    markdown_text = get_file(markdown_file)
    # html = markdown_text
    html = markdown_to_html(markdown_text)

    # result = subprocess.run([   'markdown', 
                                # markdown_file,
                                # '-h'], 
                            # stdout=subprocess.PIPE)

    # html = result.stdout.decode("utf-8")

    return html

# TEMPLATE = """
# <link rel="stylesheet" href="assets/css/markdown.css">
# <link rel="stylesheet" href="assets/css/{1}.css">
# <link rel="stylesheet" href="assets/css/{2}.css">

# <body>
  # <div class="markdown {2}">
    # {0}
  # </div>
# </body>
# """

TEMPLATE = """
<link rel="stylesheet" href="assets/css/markdown.css">
<link rel="stylesheet" href="assets/css/{1}.css">
<link rel="stylesheet" href="assets/css/{2}.css">

<style>
.center{{
    margin: auto;
    width: 50%;
    border: 2px solid #FFFFFA;
    padding: 40px;
}}
</style>

<body class="center">
  <div class="markdown-body">
    {0}
  </div>
</body>
"""
def styling(html):
    themes = [  "clearness",                # 0
                "clearness-dark",           # 1
                "github",                   # 2
                "haroopad",                 # 3
                "metro-vibes",              # 4
                "metro-vibes-dark",         # 5
                "node-dark",                # 6
                "solarized-dark",           # 7
                "solarized-light",          # 8
                "wood",                     # 9
                "wood-ri",                  # 10
                "github-dark"               # 11
                ]                          

    code_themes = [ "code-vim",             # 0
                    "code-solarized-dark",  # 1
                    "code-monokai",         # 2
                    ]

    return TEMPLATE.format( html, 
                            code_themes[2],
                            themes[11])

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
        html = markdown_file_to_html(complete_path)

        html = styling(html)

        return Response(html)
        # return Response(html, mimetype="text/markdown")
    except Exception as e:
        return Response(f"{e}")

def main():
    app.run(host='0.0.0.0', 
            port=8000)

if __name__ == '__main__':
    main()
