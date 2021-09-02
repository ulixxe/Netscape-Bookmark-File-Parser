import sys
from dataclasses import dataclass
from NetscapeBookmarkFileParser.parser import parse, NetscapeBookmark, NetscapeBookmarkFileData
from NetscapeBookmarkFileParser.exporter import netscape_html

def merge_tags(old: str, new: str):
    merged_tags = {tag.strip().casefold(): tag.strip() for tag in old.split(',')}
    for tag in new.split(','):
        if tag.strip().casefold() not in merged_tags:
            merged_tags[tag.strip().casefold()] = tag.strip()
    merged_tags.pop('', None)
    merged_tags = ','.join(merged_tags.values())
    return merged_tags

def collect_bookmarks(bookmarks_dict: dict, bookmarks_data: NetscapeBookmarkFileData, path: str = ''):
    for bookmark in bookmarks_data.bookmarks:
        if bookmark.attributes['href'] in bookmarks_dict:
            bookmarks_dict[bookmark.attributes['href']].attributes['tags'] = merge_tags(bookmarks_dict[bookmark.attributes['href']].attributes['tags'], merge_tags(bookmark.attributes.get('tags', ''), path.replace('/', ',')))
        else:
            bookmark.attributes['tags'] = merge_tags(bookmark.attributes.get('tags', ''), path.replace('/', ','))
            bookmarks_dict[bookmark.attributes['href']] = bookmark
    for sub_folder in bookmarks_data.sub_folders:
        bookmarks_dict = collect_bookmarks(bookmarks_dict, sub_folder, path+'/'+sub_folder.folder)
    return bookmarks_dict


netscape_bookmarks = parse(sys.stdin.read())
netscape_bookmarks = NetscapeBookmarkFileData(
    folder='',
    attributes={},
    description='',
    bookmarks=collect_bookmarks({}, netscape_bookmarks).values(),
    sub_folders=[],
)

print(netscape_html(netscape_bookmarks))



