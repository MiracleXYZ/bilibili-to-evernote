import json
import sys

import requests
from lxml import etree, objectify
from lxml.builder import ElementMaker
from lxml.etree import Element, ElementTree

import evernote.edam.type.ttypes as Types
from config import developer_token
from evernote.api.client import EvernoteClient
from functions import insert_img
from parse import parse_response
from utils import *

E = ElementMaker()

notebook_name = 'B博'

# 解析动态的JSON数据
dynamic_type = sys.argv[1]
dynamic_id = sys.argv[2]
dynamic_data = parse_response(dynamic_type, dynamic_id)

# Set up the NoteStore client 
client = EvernoteClient(token=developer_token, sandbox=False, china=True)
note_store = client.get_note_store()
notebooks = note_store.listNotebooks()

# 如果没有「B博」笔记本，那就创建一个
guid = ''
for notebook in notebooks:
    if notebook.name == notebook_name:
        guid = notebook.guid
if not guid:
    notebook = Types.Notebook()
    notebook.name = notebook_name
    note_store.createNotebook(notebook)
    guid = notebook.guid

note = Types.Note()
note.notebookGuid = guid
note.title = dynamic_data['content_text'].replace('\n', ' ')[:50]
if not note.resources:
    note.resources = []

# 解析xml并插入动态数据
tree = ElementTree()
if dynamic_data['origin']:
    tree.parse('./template/repost.xhtml')
else:
    tree.parse('./template/normal.xhtml')

userAvatar = tree.find('div/div[1]/div[1]/a')
userAvatar.set('href', dynamic_data['user_url'])

resource, mime, hash_hex = insert_img(dynamic_data['user_avatar'])
note.resources.append(resource)
userAvatarImg = getattr(E, 'en-media')('', {
    'style': attrib_map_avatar['style'],
    'type': mime,
    'hash': hash_hex
})
userAvatar.append(userAvatarImg)

userName = tree.find('div/div[1]/div[1]/div[1]/div[1]/a')
userName.text = dynamic_data['user_name']
userName.set('href', dynamic_data['user_url'])

publishDate = tree.find('div/div[1]/div[1]/div[1]/span')
publishDate.text = dynamic_data['publish_date']

content = tree.find('div/div[2]')
content.text = dynamic_data['content_text']

for picture in dynamic_data['pictures']:
    resource, mime, hash_hex = insert_img(picture['img_src'])
    note.resources.append(resource)
    
    contentDivImg = Element('div', attrib_map_div_img)
    contentImg = getattr(E, 'en-media')('', {
        'style': attrib_map_img['style'],
        'type': mime,
        'hash': hash_hex
    })
    contentDivImg.append(contentImg)
    content.append(contentDivImg)

dynamicLink = tree.find('div/div[3]/a')
dynamicLink.set('href', dynamic_data['dynamic_url'])

if dynamic_data['origin']:
    origin = dynamic_data['origin']
    repostUserAvatar = content.find('div/div/p/span[1]/a')
    repostUserAvatar.set('href', origin['user_url'])
    repostUserAvatar.text = origin['user_name']
    
    repostContent = content.find('div/div/p')
    repostContentText = repostContent.find('span[2]')
    repostContentText.text = origin['content_text']

    repostPublishDate = content.find('div/div/p/span[3]')
    repostPublishDate.text = origin['publish_date']

    for picture in origin['pictures']:
        resource, mime, hash_hex = insert_img(picture['img_src'])
        note.resources.append(resource)
        
        repostContentDivImg = Element('div', attrib_map_repost_div_img)
        repostContentImg = getattr(E, 'en-media')('', {
            'style': attrib_map_repost_img['style'],
            'type': mime,
            'hash': hash_hex
        })
        repostContentDivImg.append(repostContentImg)
        repostContent.append(repostContentDivImg)

note.content = etree.tostring(tree).decode('utf8')

# 完成笔记创建过程
note_store.createNote(note)
