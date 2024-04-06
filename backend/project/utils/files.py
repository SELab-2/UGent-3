"""Utility functions for files"""

from os.path import getsize
from re import match
from typing import List, Optional
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED, is_zipfile
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def all_files_uploaded(files: List[FileStorage], regexes: List[str]) -> bool:
    """Check if all the required files are uploaded

    Args:
        files (List[FileStorage]): The files uploaded
        regexes (List[str]): The list of regexes to match against

    Returns:
        bool: Are all required files uploaded
    """

    all_filenames = []
    for file in files:
        # Zip
        if is_zipfile(file):
            with ZipFile(file, "r") as zip_file:
                all_filenames += zip_file.namelist()
        # File
        else:
            all_filenames.append(file.filename)

    for regex in regexes:
        match_found = any(match(regex, name) is not None for name in all_filenames)
        if not match_found:
            return False

    return True

def zip_files(name: str, files: List[FileStorage]) -> Optional[FileStorage]:
    """Zip a dictionary of files

    Args:
        files (List[FileStorage]): The files to be zipped

    Returns:
        FileStorage: The zipped file
    """

    compression = ZIP_DEFLATED # Compression algorithm
    zip64 = False # Extension for larger files and archives (now limited to 4GB)
    level = None # Compression level, None = default

    try:
        buffer = BytesIO()
        with ZipFile(buffer, "w", compression, zip64, level) as zip_file:
            for file in files:
                filename = secure_filename(file.filename)
                zip_file.writestr(filename, file.stream.read())
        zip_file = FileStorage(buffer, name)

        return zip_file
    except IOError:
        return None
