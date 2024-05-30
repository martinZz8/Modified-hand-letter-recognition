from models.Prediction import Prediction
from exceptions.CustomExceptions import BadInputException


def predictionToDTO(org_pred: Prediction):
    return {
        "id": org_pred.id,
        "image_name": org_pred.image_current_fullname,
        "predicted_class": org_pred.predicted_class,
        "predicted_successful": org_pred.predicted_successful,
        "evaluation_datetime": org_pred.evaluation_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    }


def strToBool(input_str: str, fieldName: str = None) -> bool:
    lower_input_str = input_str.lower()

    if lower_input_str == "true":
        return True
    elif lower_input_str == "false":
        return False

    raise BadInputException(f"strToBool{f' [fieldName={fieldName}]' if fieldName is not None else ''}: Wrong input parameter - has to be either \"true\" or \"false\"")


def strToInt(input_str: str, fieldName: str = None) -> bool:
    if input_str.isdigit():
        return True

    raise BadInputException(f"strToInt{f' [fieldName={fieldName}]' if fieldName is not None else ''}: Wrong input parameter - has to be integer representation of string")
