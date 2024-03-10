"""Utility functions for files"""

from re import match
from typing import List, Union
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

def check_filename(filename: str, regexes: List[str]) -> bool:
    """Check if the filename 

    Args:
        filename (str): The filename
        regex_list (List[str]): A list of regexes to match against

    Returns:
        bool: Is the filename ok
    """

    # Return true if the filename matches for all regexes
    return all(map(lambda regex: match(regex, filename) is not None, regexes))

def all_files_uploaded(files: List[FileStorage], regexes: List[str]) -> bool:
    """Check if all the required files are uploaded

    Args:
        files (List[FileStorage]): The files uploaded
        regexes (List[str]): The list of regexes to match against

    Returns:
        bool: Are all required files uploaded
    """

    all_uploaded = True
    for regex in regexes:
        match_found = any(match(regex, file.filename) is not None for file in files)
        if not match_found:
            all_uploaded = False
            break
    return all_uploaded

def zip_files(name: str, files: List[FileStorage]) -> Union[FileStorage, None]:
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
