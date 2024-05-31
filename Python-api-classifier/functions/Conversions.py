from typing import Optional
from models.Prediction import Prediction
from exceptions.CustomExceptions import BadInputException


def predictionToDTO(org_pred: Prediction):
    return {
        "id": org_pred.id,
        "image_name": org_pred.image_current_fullname,
        "predicted_class": org_pred.predicted_class,
        "predicted_successful": org_pred.predicted_successful,
        "evaluation_datetime_utc": org_pred.evaluation_datetime_utc.strftime("%d/%m/%Y, %H:%M:%S"),
        "execution_length_sec": org_pred.execution_length_sec,
        "used_cuda": org_pred.used_cuda
    }


def strToBool(input_str: Optional[str], fieldName: str = None, isOptional: bool = False) -> Optional[bool]:
    if input_str is None:
        if isOptional:
            return None

        raise BadInputException(f"strToBool{f' [{fieldName}]' if fieldName is not None else ''}: Field is mandatory")

    lower_input_str = input_str.lower()
    if lower_input_str == "true":
        return True
    elif lower_input_str == "false":
        return False

    raise BadInputException(f"strToBool{f' [{fieldName}]' if fieldName is not None else ''}: Wrong input parameter - has to be either 'true' or 'false'")


def strToInt(input_str: Optional[str], fieldName: str = None, isOptional: bool = False) -> Optional[int]:
    if input_str is None:
        if isOptional:
            return None

        raise BadInputException(f"strToInt{f' [{fieldName}]' if fieldName is not None else ''}: Field is mandatory")

    if input_str.isdigit():
        return int(input_str)

    raise BadInputException(f"strToInt{f' [{fieldName}]' if fieldName is not None else ''}: Wrong input parameter - has to be integer representation of string")

