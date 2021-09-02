# Netscape-Bookmark-File-Parser
NetscapeBookmarkFileParser is a Netscape Bookmark File parser that reads and populates bookmarks info in the dataclass:
```
@dataclass
class NetscapeBookmark:
    title: str
    attributes: dict
    description: str
```
It manages nested folders by populating the dataclass:
```
@dataclass
class NetscapeBookmarkFileData:
    folder: str
    attributes: dict
    description: str
    bookmarks: [NetscapeBookmark]
    sub_folders: [Type['NetscapeBookmarkFileData']]
```
Through these dataclass, it is possible to modify bookmarks files.

`folders2labels.py` script generates a flat file structure from one with nested folders. Folders are converted to tags.

The command line to convert `bookmarks_in.html` to `bookmarks_out.html` is:
```
python3 folders2tags.py < bookmarks_in.html > bookmarks_out.html
```
