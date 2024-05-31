from typing import List
from werkzeug.datastructures.file_storage import FileStorage
from exceptions.CustomExceptions import BadInputException

acceptable_file_extensions = ["png", "jpg", "jpeg", "bmp"]


def checkIfProperImageFileExists(files: List[FileStorage], fieldName: str = None) -> bool:
    if len(files) == 0:
        raise BadInputException(f"checkIfProperImageFileExists{f' [{fieldName}]' if fieldName is not None else ''}: no file was provided")

    if len(files) > 1:
        raise BadInputException(f"checkIfProperImageFileExists{f' [{fieldName}]' if fieldName is not None else ''}: you can provide only one file")

    file_extension = files[0].filename.split(".")[-1]
    if file_extension in acceptable_file_extensions:
        return True

    raise BadInputException(f"checkIfProperImageFileExists{f' [{fieldName}]' if fieldName is not None else ''}: given file has wrong extension (accepted are: {', '.join(acceptable_file_extensions)})")
