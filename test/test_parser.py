from dataclasses import dataclass

import sys as sys
sys.path.append('../')

from NetscapeBookmarkFileParser.parser import parse
from NetscapeBookmarkFileParser.exporter import netscape_html

with open ("bookmarks.html", "r") as myfile:
    html=myfile.read()


netscape_bookmarks = parse(html)

print(netscape_html(netscape_bookmarks))
