from exceptions.CustomExceptions import BadInputException

acceptable_file_extensions = ["png", "jpg", "jpeg", "bmp"]


def checkIfProperImageFileExists(file, fieldName: str = None) -> bool:
    if file is None:
        raise BadInputException(
            f"checkIfProperImageFileExists{f' [fieldName={fieldName}]' if fieldName is not None else ''}: field is empty")

    file_extension = file.filename.split(".")[-1]
    isAcceptable = file_extension in acceptable_file_extensions

    if isAcceptable:
        return True

    raise BadInputException(
        f"checkIfProperImageFileExists{f' [fieldName={fieldName}]' if fieldName is not None else ''}: has wrong file extension (accepted are: {', '.join(acceptable_file_extensions)})")
