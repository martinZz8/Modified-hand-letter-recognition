# Connecting SQLAlchemy with MySQL: https://planetscale.com/blog/using-mysql-with-sql-alchemy-hands-on-examples
# Env variables loading: https://developer.vonage.com/en/blog/python-environment-variables-a-primer
# How to use SQLAlchemy 2.0: https://planetscale.com/blog/using-mysql-with-sql-alchemy-hands-on-examples

# Note:
# - server works as host: localhost:5000
from typing import List
from dotenv import load_dotenv
import os
from os.path import dirname, join, exists
from os import remove
import uuid
import subprocess
from flask import Flask, request, Response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session
from json import dumps
from models.BaseModel import BaseModel
from models.Prediction import Prediction
from exceptions.CustomExceptions import BadInputException

from functions.Conversions import predictionToDTO, strToBool, strToInt
from functions.Validators import checkIfProperImageFileExists


# -- Load env variables --
load_dotenv()  # This line brings all environment variables from ".env" file into "os.environ"
mySqlConnStr = os.environ["MYSQL_CONN_STR"]

# -- Create SQLAlchemy engine (with model schema) --
SQLAlchemyEngine = create_engine(mySqlConnStr, echo=True)
BaseModel.metadata.create_all(SQLAlchemyEngine)

# -- Create Flask application (no runtime yet) --
app = Flask(__name__)

# -- Connect Flask app with Flask-Migrate tool --
# Note: "db" and "migrate" variables are only used to create migrations via the "flask" cmd tool
app.config['SQLALCHEMY_DATABASE_URI'] = mySqlConnStr
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# -- Define Flask routes --
@app.route('/prediction', methods=['GET'])
def getAllPredictions():
    with Session(SQLAlchemyEngine) as session:
        # Get all predictions
        predictions: List[Prediction] = session.scalars(select(Prediction)).all()

        # Convert to DTO dictionaries
        predictionsDTO = list(map(lambda x: predictionToDTO(x), predictions))

        # Return results
        return jsonify(predictionsDTO)  # or use: Response(dumps(dictData), status=200, mimetype='application/json') - "Response" is imported from flask; "dumps" is imported from "json"


@app.route('/prediction/<int:id>', methods=['GET'])
def getPredictionById(id: int):
    with Session(SQLAlchemyEngine) as session:
        # Create select query for Prediction by id
        query = select(Prediction).where(Prediction.id == id)
        prediction: Prediction = session.scalars(query).first()

        print(f"Prediction object: {prediction}")  # TODO - delete the print after end of code debugging
        # Check if response exists - if not, return error and no data
        if prediction is None:
            resData = {
                "data": None,
                "error_message": "Item with given id doesn't exist"
            }

            return Response(dumps(resData), status=404, mimetype="application/json")

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
        prediction: Prediction = session.scalars(query).first()

        # Check if response exists - if not, return error and no data
        if prediction is None:
            resData = {
                "error_message": "Item with given id doesn't exist"
            }

            return Response(dumps(resData), status=404, mimetype="application/json")

        # Delete found prediction
        query = delete(Prediction).where(Prediction.id == id)
        session.execute(query)

        # Commit changes  to DB
        session.commit()

        # Delete image from folder "stored_images"
        path_to_images = join(dirname(__file__), "stored_images")
        image_path_to_delete = join(path_to_images, prediction.image_current_fullname)

        if exists(image_path_to_delete):
            remove(image_path_to_delete)

        # Prepare response and return it
        resData = {
            "error_message": None
        }

        return jsonify(resData)


@app.route('/prediction', methods=['POST'])
def createPrediction():
    with Session(SQLAlchemyEngine) as session:
        # Get all parameters from body (also validate them)
        # This parameters (and some other ones) will be passed as the input args of program "Python-eval-all\single-classify\main-single.py"
        try:
            bodyParams = {
                "useMediaPipe": strToBool(request.form.get("useMediaPipe"), fieldName="useMediaPipe"),
                "modelVersion": strToInt(request.form.get("modelVersion"), fieldName="modelVersion", isOptional=True),
                "losoModelPerson": strToInt(request.form.get("losoModelPerson"), fieldName="losoModelPerson", isOptional=True),
                "preprocessing": strToBool(request.form.get("usePreprocessing"), fieldName="usePreprocessing"),
                "shiftedData": strToBool(request.form.get("useShiftedData"), fieldName="useShiftedData"),
                "skeletonRescale": strToBool(request.form.get("useSkeletonRescale"), fieldName="useSkeletonRescale"),  # if "false", we use "imageResize"
                "cuda": strToBool(request.form.get("useCuda"), fieldName="useCuda"),  # if "false", we use "cpu"
                # Files exctracted like: https://stackoverflow.com/questions/11817182/uploading-multiple-files-with-flask
                "inputFile": request.files.get("file") if checkIfProperImageFileExists(request.files.getlist("file"), fieldName="file") else None
            }
            print(f"bodyParams: {bodyParams}")
        except BadInputException as err:
            resData = {
                "data": None,
                "error_message": str(err)
            }

            return Response(dumps(resData), status=404, mimetype="application/json")

        # Generate id for image and save it in "stored_images" folder
        # Also form absolute paths for input image and saved results of classification
        inputFolderPath = join(dirname(__file__), "stored_images")
        inputImageId = str(uuid.uuid4())
        imageExtensionName = bodyParams['inputFile'].filename.split('.')[-1]
        inputImageName = f"{inputImageId}.{imageExtensionName}"
        inputImagePath = join(inputFolderPath, inputImageName)

        outputFolderPath = join(dirname(dirname(__file__)), "Python-eval-all", "single-classify", "output")
        outputFileName = "results.txt"
        outputFilePath = join(outputFolderPath, outputFileName)

        # Save image to "stored_image" folder (with conversion current file stored in memory to binary hex string)
        # Alternative option to save image from "FileStorage" object: "bodyParams["inputFile"].save(inputImagePath)" (from: https://stackoverflow.com/questions/18249949/python-file-object-to-flasks-filestorage)
        with open(inputImagePath, 'wb') as f:
            binaryHexStr = bodyParams["inputFile"].read()
            f.write(binaryHexStr)

        # Execute classification model and read results
        # Determine arguments for classification script
        scriptCwd = dirname(outputFolderPath)

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
                predicted_class=None,
                predicted_successful=False,
                execution_length_sec=None,
                used_cuda=bodyParams["cuda"]
            )
            session.add(predictionToAdd)

            # Commit changes to DB
            session.commit()

            return Response(dumps(resData), status=404, mimetype="application/json")

        # Otherwise, just add new, successful prediction
        # Read classification result from output text file
        with open(outputFilePath, 'r') as f:
            allLines = f.readlines()

        hasOutputFileProperFormat = True
        try:
            predictedLetter = allLines[0].split(":")[1].strip()
            executionLength = float(allLines[1].split(":")[1].strip().split(" ")[0])
        except (IndexError, ValueError):
            hasOutputFileProperFormat = False

        if hasOutputFileProperFormat:
            # Prepare Prediction object and add it to DB
            predictionToAdd = Prediction(
                image_id=inputImageId,
                image_current_fullname=inputImageName,
                image_original_fullname=bodyParams["inputFile"].filename,
                predicted_class=predictedLetter,
                predicted_successful=True,
                execution_length_sec=executionLength,
                used_cuda=bodyParams["cuda"]
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
            "error_message": "Image prediction was run, but output file has improper format"
        }

        return Response(dumps(resData), status=404, mimetype="application/json")


if __name__ == '__main__':
    # -- Run Flask app --
    app.run(debug=True)
