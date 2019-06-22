import binascii
import hashlib
import os
from io import BytesIO
from urllib.request import urlopen

import requests
from PIL import Image

import evernote.edam.type.ttypes as Types


def insert_img(url):
    with urlopen(url) as image_url:
        tempimg = 'temp.' + url.split('.')[-1]
        with open(tempimg, 'wb') as f:
            f.write(image_url.read())
    # To include an attachment such as an image in a note, first create a Resource
    # for the attachment. At a minimum, the Resource contains the binary attachment
    # data, an MD5 hash of the binary data, and the attachment MIME type.
    # It can also include attributes such as filename and location.
    image = open(tempimg, 'rb').read()
    md5 = hashlib.md5()
    md5.update(image)
    hash_ = md5.digest()

    data = Types.Data()
    data.size = len(image)
    data.bodyHash = hash_
    data.body = image

    image_type = url.split('.')[-1]
    if image_type == 'jpg' or image_type == 'jpeg':
        mime = 'image/jpeg'
    elif image_type == 'png':
        mime = 'image/png'
    elif image_type == 'gif':
        mime = 'image/gif'
    else:
        raise ValueError

    resource = Types.Resource()
    resource.mime = mime
    resource.data = data

    # To display the Resource as part of the note's content, include an <en-media>
    # tag in the note's ENML content. The en-media tag identifies the corresponding
    # Resource using the MD5 hash.
    hash_hex = binascii.hexlify(hash_)

    os.remove(tempimg)

    return resource, mime, hash_hex.decode('utf8')
