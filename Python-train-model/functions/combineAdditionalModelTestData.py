import functools


def combineAdditionalModelTestData(allDrawnTestIdxs: list,
                                   y_true: list,
                                   y_pred: list,
                                   availableLetters: list):
    # Combine "allDrawnTestIdxsStr"
    allDrawnTestIdxsStr = "[\n"

    for i, letterIdxs in enumerate(allDrawnTestIdxs):
        allDrawnTestIdxsStr += "\t["
        allDrawnTestIdxsStr += ', '.join([str(x) for x in letterIdxs])
        allDrawnTestIdxsStr += "]"

        if i != (len(allDrawnTestIdxs) - 1):
            allDrawnTestIdxsStr += ","
        allDrawnTestIdxsStr += "\n"

    allDrawnTestIdxsStr += "]"

    # Combine y_true and y_pred
    predictedValues = ""

    numOfPredictedGood = functools.reduce(lambda acc, x: acc + 1 if x[0] == x[1] else acc, zip(y_true, y_pred), 0)
    numOfAllElements = len(y_true)

    for idx, (single_y_true, single_y_pred) in enumerate(zip(y_true, y_pred)):
        predictedValues += f"{idx+1}) y_true={availableLetters[single_y_true]}, y_pred={availableLetters[single_y_pred]}"

        if idx != (numOfAllElements - 1):
            predictedValues += "\n"

    return f"AllDrawnTestIdxs (each row corresponds to letter ordered in alphabetical order):\n{allDrawnTestIdxsStr}\n\n" \
           f"True and predicted values (during test):\n" \
           f"Model predicted well {numOfPredictedGood} of {numOfAllElements} elements ({(numOfPredictedGood / numOfAllElements)*100:.2f}% acc)\n" \
           f"{predictedValues}"
