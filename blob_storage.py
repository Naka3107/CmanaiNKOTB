#coding: UTF-8

import os, inspect
from azure.storage.blob import *

MY_ACCOUNT = 'nkotb'
KEY = 'BfGLrqVE/pSRbMa7zrcILjU75LY5ZUKg4amsRJ8k3nf5PHdpmVc+FVjtOJ9fK9eLj3zLe7hegu3cm8eLZUFaAw=='
MY_CONTAINER = 'storage'
URL = 'https://nkotb.blob.core.windows.net/storage/'
# https://nkotb.blob.core.windows.net/storage/hermosa.jpg

def uploadImage(newName, imageName):

    try:
        block_blob_service = BlockBlobService(account_name=MY_ACCOUNT, account_key=KEY)

        # The same containers can hold all types of blobs
        block_blob_service.create_container(MY_CONTAINER, public_access=PublicAccess.Container)

        block_blob_service.create_blob_from_path(
            MY_CONTAINER,
            newName,
            './Images/' + imageName,
            content_settings=ContentSettings(content_type='image/jpg')
        )

        print "Upload exitoso!"

    except Exception as e:
        print "Upload error:: " + e.message + " // " + e.message

uploadImage('tierna', 'b2')

# block_blob_service.delete_blob('mycontainer', 'myblockblob')