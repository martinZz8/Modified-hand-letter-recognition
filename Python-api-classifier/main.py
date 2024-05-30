# Connecting SQLAlchemy with MySQL: https://planetscale.com/blog/using-mysql-with-sql-alchemy-hands-on-examples
# Env variables loading: https://developer.vonage.com/en/blog/python-environment-variables-a-primer
# How to use SQLAlchemy 2.0: https://planetscale.com/blog/using-mysql-with-sql-alchemy-hands-on-examples
from dotenv import load_dotenv
import os
from os.path import dirname, join
import uuid
import subprocess
import codecs
from flask import Flask, request, Response, jsonify
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session
from json import dumps
from models.BaseModel import BaseModel
from models.Prediction import Prediction
from exceptions.CustomExceptions import BadInputException

from functions.Conversions import predictionToDTO, strToBool, strToInt
from functions.Validators import checkIfProperImageFileExists

if __name__ == '__main__':
    # -- Load env variables --
    load_dotenv()  # This line brings all environment variables from .env into os.environ
    mySqlConnStr = os.environ["MYSQL_CONN_STR"]

    # -- Create SQLAlchemy engine (with model schema) --
    SQLAlchemyEngine = create_engine(mySqlConnStr, echo=True)
    BaseModel.metadata.create_all(SQLAlchemyEngine)

    # -- Create Flask application (no runtime yet) --
    app = Flask(__name__)

    # -- Define Flask routes --
    @app.route('/prediction', methods=['GET'])
    def getAllPredictions():
        with Session(SQLAlchemyEngine) as session:
            # Get all predictions
            predictions = session.scalars(select(Prediction))

            # Convert to DTO dictionaries
            predictionsDTO = list(map(lambda x: predictionToDTO(x), predictions))

            # Return results
            return jsonify(predictionsDTO)  # or use: Response(dumps(dictData), status=200, mimetype='application/json') - "Response" is imported from flask; "dumps" is imported from "json"


    @app.route('/prediction/<int:id>', methods=['GET'])
    def getPredictionById(id: int):
        with Session(SQLAlchemyEngine) as session:
            # Create select query for Prediction by id
            query = select(Prediction).where(Prediction.id == id)
            prediction = session.scalars(query)

            # Check if response exists - if not, return error and no data
            if prediction in None:
                resData = {
                    "data": None,
                    "error_message": "Item with given id doesn't exist"
                }

                return Response(dumps(resData), status=404)

            # Prepare response and return it
            resData = {
                "data": predictionToDTO(prediction),
                "error_message": None
            }

            return jsonify(resData)

    @app.route('/prediction/<int:id>', methods=['DELETE'])
    def deletePredictionById(id: int):
        with Session(SQLAlchemyEngine) as session:
            # Create select query for Prediction by id
            query = select(Prediction).where(Prediction.id == id)
            prediction = session.scalars(query)

            # Check if response exists - if not, return error and no data
            if prediction in None:
                resData = {
                    "error_message": "Item with given id doesn't exist"
                }

                return Response(dumps(resData), status=404)

            # Delete found prediction
            delete(Prediction).where(Prediction.id == id)

            # Commit changes  to DB
            session.commit()

            # Prepare response and return it
            resData = {
                "error_message": None
            }

            return jsonify(resData)

    @app.route('/prediction', methods=['PUT'])
    def createPrediction():
        with Session(SQLAlchemyEngine) as session:
            # Get all parameters from body (also validate them)
            # This parameters (and some other ones) will be passed as the input args of program "Python-eval-all\single-classify\main-single.py"
            try:
                bodyParams = {
                    "useMediaPipe": strToBool(request.form["useMediaPipe"], fieldName="useMediaPipe"),
                    "modelVersion": strToInt(request.form["modelVersion"]) if request.form["modelVersion"] is not None else None,
                    "losoModelPerson": strToInt(request.form["losoModelPerson"]) if request.form["losoModelPerson"] is not None else None,
                    "preprocessing": strToBool(request.form["usePreprocessing"], fieldName="usePreprocessing"),
                    "shiftedData": strToBool(request.form["useShiftedData"], fieldName="useShiftedData"),
                    "skeletonRescale": strToBool(request.form["useSkeletonRescale"], fieldName="useSkeletonRescale"),  # if "false", we use "imageResize"
                    "cuda": strToBool(request.form["useCuda"], fieldName="useCuda"),  # if "false", we use "cpu"
                    "inputFile": request.files["file"] if checkIfProperImageFileExists(request.files["file"]) else None
                }
            except BadInputException as err:
                resData = {
                    "data": None,
                    "error_message": err
                }

                return Response(dumps(resData), status=404)

            # Generate id for image and save it in "stored_images" folder
            # Also form absolute paths for input image and saved results of classification
            inputFolderPath = join(dirname(__file__), "stored_images")
            inputImageId = uuid.uuid4()
            imageExtensionName = bodyParams['inputFile'].filename.split('.')[-1]
            inputImageName = f"{inputImageId}.{imageExtensionName}"
            inputImagePath = join(inputFolderPath, inputImageName)

            outputFolderPath = join(dirname(dirname(__file__)), "Python-eval-all", "single-classify", "output")
            outputFileName = "results.txt"
            outputFilePath = join(outputFolderPath, outputFileName)

            # Save image to "stored_image" folder (with conversion current file stored in memory to binary hex string)
            with open(inputImagePath, 'wb') as f:
                binaryHexStr = codecs.encode(bodyParams["inputFile"], "hex_codec")
                print(f"binaryHexStr: {binaryHexStr}")  # TODO - delete the print after end of code debugging
                f.write(binaryHexStr)

            # Execute classification model and read results
            # Determine arguments for classification script
            scriptCwd = dirname(outputFolderPath)
            print(f"scriptCwd: {scriptCwd}")  # TODO - delete the print after end of code debugging

            scriptProgramName = "py"
            scriptPythonVersion = "-3"
            scriptName = "main-single.py"
            scriptAddParameters = [
                '-m' if bodyParams["useMediaPipe"] else '-o',
                '-v' if bodyParams["modelVersion"] is not None else '',
                str(bodyParams["modelVersion"]) if bodyParams["modelVersion"] is not None else '',
                '-l' if bodyParams["losoModelPerson"] is not None else '',
                str(bodyParams["losoModelPerson"]) if bodyParams["losoModelPerson"] is not None else '',
                '-p' if bodyParams["preprocessing"] else '-P',
                '-s' if bodyParams["shiftedData"] else '-S',
                '-f',
                inputFolderPath,
                '-i',
                inputImageName,
                '-t',
                outputFileName,
                '-R' if bodyParams["skeletonRescale"] else '-r',
                '-c' if bodyParams["cuda"] else '-C'
            ]
            scriptAddParameters = list(filter(lambda x: len(x) > 0, scriptAddParameters))

            # Run Python classifier script
            # Also note, how to throw stdout from subprocess away: https://stackoverflow.com/questions/7082623/suppress-output-from-subprocess-popen
            lsOutput = subprocess.Popen([scriptProgramName, scriptPythonVersion, scriptName] + scriptAddParameters, cwd=scriptCwd)
            lsOutput.communicate()  # Will block for 30 seconds
            rc = lsOutput.returncode

            # Check if prediction is successful - if not, add unsuccessful prediction and return error
            if rc != 0:
                # Error during runtime
                resData = {
                    "data": None,
                    "error_message": "Couldn't predict image properly"
                }

                # Add unsuccessful prediction
                predictionToAdd = Prediction(
                    image_id=inputImageId,
                    image_current_fullname=inputImageName,
                    image_original_fullname=bodyParams["inputFile"].filename,
                    predicted_class="",
                    predicted_successful=False
                )
                session.add(predictionToAdd)

                # Commit changes to DB
                session.commit()

                return Response(dumps(resData), status=404)

            # Otherwise, just add new, successful prediction
            # Read classification result from output text file
            with open(outputFilePath, 'r') as f:
                firstLine = f.readline()
                splittedFirstLine = firstLine.split(":")

                if len(splittedFirstLine) == 2:
                    predictedLetter = splittedFirstLine[1].strip()

                    # Prepare Prediction object and add it to DB
                    predictionToAdd = Prediction(
                        image_id=inputImageId,
                        image_current_fullname=inputImageName,
                        image_original_fullname=bodyParams["inputFile"].filename,
                        predicted_class=predictedLetter,
                        predicted_successful=True
                    )
                    session.add(predictionToAdd)

                    # Commit changes to DB
                    session.commit()

                    # Prepare response and return it
                    resData = {
                        "data": predictionToDTO(predictionToAdd),
                        "error_message": None
                    }

                    return jsonify(resData)
                
                # Output file has wrong format
                resData = {
                    "data": None,
                    "error_message": "Image prediction was run, but output file has wrong format"
                }

                return Response(dumps(resData), status=404)

    # -- Run Flask app --
    app.run(debug=True)
