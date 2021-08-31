from typing import List

from NetscapeBookmarkFileParser.parser import NetscapeBookmark, NetscapeBookmarkFileData

BookmarkDocument = List[str]


def netscape_html(netscape_data: NetscapeBookmarkFileData) -> str:
    doc = []
    append_header(doc)
    doc.append('')
    append_netscape_data(doc, netscape_data)

    return '\n'.join(doc)

def append_netscape_data(doc: BookmarkDocument, netscape_data: NetscapeBookmarkFileData, indent: str = ''):
    if netscape_data.folder != '':
        attributes = " ".join([f'{key.upper()}="{value}"' for (key,value) in netscape_data.attributes.items()])
        doc.append(f'{indent}<DT><H3 {attributes}>{netscape_data.folder}</H3>')
        if netscape_data.description:
            doc.append(f'{indent}<DD>{netscape_data.description}')
    doc.append(f'{indent}<DL><p>')
    [append_bookmark(doc, bookmark, indent+"    ") for bookmark in netscape_data.bookmarks]
    for sub_folder in netscape_data.sub_folders:
        append_netscape_data(doc, sub_folder, indent+"    ")
    doc.append(f'{indent}</DL><p>')


def append_header(doc: BookmarkDocument):
    doc.append('<!DOCTYPE NETSCAPE-Bookmark-file-1>')
    doc.append('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">')
    doc.append('<TITLE>Bookmarks</TITLE>')
    doc.append('<H1>Bookmarks</H1>')


def append_bookmark(doc: BookmarkDocument, bookmark: NetscapeBookmark, indent: str = ''):
    attributes = " ".join([f'{key.upper()}="{value}"' for (key,value) in bookmark.attributes.items()])
    doc.append(f'{indent}<DT><A {attributes}>{bookmark.title}</A>')
    if bookmark.description:
        doc.append(f'{indent}<DD>{bookmark.description}')
