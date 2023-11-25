import functools
import random


def determineBestModel(modelDatas: list):
    modelDataToRet = None

    if len(modelDatas) > 0:
        if len(modelDatas) == 1:
            modelDataToRet = modelDatas[0]
        else:
            # Determine biggest train acc and elements with that value
            allTrainAcc = list(map(lambda x: x["tracked_train_values_li"][-1]["acc"], modelDatas))
            biggestTrainAcc = functools.reduce(lambda actMax, x: x if x > actMax else actMax, allTrainAcc)
            modelDatasWithBiggestTrainAcc = list(filter(lambda x: x["tracked_train_values_li"][-1]["acc"] == biggestTrainAcc, modelDatas))

            # Check whether is one or more elements with biggest train acc
            # If are more - compare test acc of them. Otherwise get first element
            if len(modelDatasWithBiggestTrainAcc) > 1:
                # Determine biggest test acc of selected elements and get those elements
                selectedTestAcc = list(map(lambda x: x["tracked_test_values"]["acc"], modelDatasWithBiggestTrainAcc))
                biggestTestAcc = functools.reduce(lambda actMax, x: x if x > actMax else actMax, selectedTestAcc)
                selectedModelDatasWithBiggestTestAcc = list(filter(lambda x: x["tracked_test_values"]["acc"] == biggestTestAcc, modelDatasWithBiggestTrainAcc))

                # Check whether is one or more selected elements with biggest test acc
                # If are more - get random element. Otherwise get first element
                if len(selectedModelDatasWithBiggestTestAcc) > 1:
                    randIdx = random.randint(0, len(selectedModelDatasWithBiggestTestAcc) - 1)
                    modelDataToRet = selectedModelDatasWithBiggestTestAcc[randIdx]
                else:
                    modelDataToRet = selectedModelDatasWithBiggestTestAcc[0]
            else:
                modelDataToRet = modelDatasWithBiggestTrainAcc[0]

    return modelDataToRet
