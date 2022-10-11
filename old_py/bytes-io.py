#!/usr/bin/env python3
from io import BytesIO
import shutil
# Initialie our BytesIO
myio = BytesIO()
myio.write(b"Test 123")
def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())
        write_bytesio_to_file("out.txt", myio)
