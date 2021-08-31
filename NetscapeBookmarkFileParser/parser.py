from dataclasses import dataclass
from typing import Type

import pyparsing as pp


@dataclass
class NetscapeBookmark:
    title: str
    attributes: dict
    description: str

@dataclass
class NetscapeBookmarkFileData:
    folder: str
    attributes: dict
    description: str
    bookmarks: [NetscapeBookmark]
    sub_folders: [Type['NetscapeBookmarkFileData']]


def extract_folder_data(tokens):
    bookmarks = []
    sub_folders = []
    for elem in tokens.folder_items:
        if elem['type'] == "bookmark":
            bookmarks.append(elem['data'])
        else:
            sub_folders.append(elem['data'])
    return NetscapeBookmarkFileData(folder='',
                                    attributes={},
                                    description='',
                                    bookmarks=bookmarks,
                                    sub_folders=sub_folders,
                                    )


# define grammar
dt_start, _ = pp.makeHTMLTags("DT")
dd_start, _ = pp.makeHTMLTags("DD")
description = dd_start + pp.SkipTo(pp.anyOpenTag | pp.anyCloseTag)("description")
description.setParseAction(lambda tokens: tokens.description.strip())

a_start, a_end = pp.makeHTMLTags("A")
bookmark_link = a_start + a_start.tag_body("text") + a_end.suppress()
bookmark_link.setParseAction(lambda tokens: {key:value for (key,value) in tokens.items() if (isinstance(value, str) and key != 'tag')})

bookmark = dt_start + bookmark_link("link") + pp.ZeroOrMore(description)("description")
bookmark.setParseAction(lambda tokens: {'type': "bookmark",
                                        'data': NetscapeBookmark(title=tokens.link['text'],
                                                                 attributes={key:value for (key,value) in tokens.link.items() if key != 'text'},
                                                                 description=tokens.description[0] if tokens.description else '',
                                                                 ),
                                        })

p_start, _ = pp.makeHTMLTags("p")
dl_start, dl_end = pp.makeHTMLTags("DL")
folder = pp.Forward()
folder_data = dl_start + p_start + pp.Group(pp.ZeroOrMore(bookmark | folder))("folder_items") + dl_end + pp.Optional(p_start)
folder_data.setParseAction(extract_folder_data)

h3_start, h3_end = pp.makeHTMLTags("H3")
folder_name = h3_start + h3_start.tag_body("text") + h3_end.suppress()
folder_name.setParseAction(lambda tokens: {key:value for (key,value) in tokens.items() if (isinstance(value, str) and key != 'tag')})

folder << dt_start + folder_name("folder_name") + pp.ZeroOrMore(description)("description") + folder_data("data")
folder.setParseAction(lambda tokens: {'type': "folder",
                                      'data': NetscapeBookmarkFileData(
                                          folder=tokens.folder_name['text'],
                                          attributes={key:value for (key,value) in tokens.folder_name.items() if key != 'text'},
                                          description=tokens.description[0] if tokens.description else '',
                                          bookmarks=tokens.data.bookmarks,
                                          sub_folders=tokens.data.sub_folders,
                                      )})


def parse(html: str) -> NetscapeBookmarkFileData:
    return folder_data.searchString(html)[0][0]
