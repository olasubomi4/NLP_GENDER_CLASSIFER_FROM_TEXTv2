import azure.functions as func
import logging

from dotenv import load_dotenv
import joblib
import os
import json
from sentence_transformers import SentenceTransformer
from dto.ResponseObject import ResponseObject
from service.PredictorService import PredictorService
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="HttpTrigger1")
@app.route('v1/predictGender', methods=['POST'])
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    load_dotenv()
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(f'Model path {os.getcwd()+os.getenv("ML_MODEL_PATH")}')
    ml_model=joblib.load(os.getcwd()+os.getenv("ML_MODEL_PATH"))
    encoder=SentenceTransformer("paraphrase-mpnet-base-v2")
    responseObject = ResponseObject()
    req_body = req.get_json()

    try:
        blog_text =req_body.get('blogText')
        predictor_service = PredictorService(encoder, ml_model)
        prediction = predictor_service.predict([blog_text])
        responseObject.setResponseMessage("Action successful")
        responseObject.setResponseStatus(True)
        gender = {
            "Gender": f"{prediction}"
        }
        responseObject.setData(gender)
    except Exception as e:
        logging.error(e)
        responseObject.setResponseStatus(False)
        responseObject.setResponseMessage(f"Could not process the request. Please try again later. Due to {e}")

    logging.info(responseObject.jsonfyResponse())
    return func.HttpResponse(json.dumps(responseObject.jsonfyResponse()), status_code=200, mimetype="application/json")

@app.function_name(name="HttpTrigger2")
@app.route('v1/predictGenders', methods=['POST'])
def get_genders(req: func.HttpRequest) -> func.HttpResponse:
    load_dotenv()
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(f'Model path {os.getcwd() + os.getenv("ML_MODEL_PATH")}')
    ml_model = joblib.load(os.getcwd() + os.getenv("ML_MODEL_PATH"))
    encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
    responseObject = ResponseObject()
    req_body = req.get_json()
    try:
        blog_text=req_body.get('blogTexts')
        predictor_service= PredictorService(encoder,ml_model)
        prediction=predictor_service.predict2(blog_text)
        responseObject.setResponseMessage("Action successful")
        responseObject.setResponseStatus(True);
        responseObject.setData(prediction)
    except Exception as e:
        responseObject.setResponseStatus(False)
        responseObject.setResponseMessage(f"Could not process the request. Please try again later. Due to {e}")

    logging.info(responseObject.jsonfyResponse())
    return func.HttpResponse(json.dumps(responseObject.jsonfyResponse()), status_code=200, mimetype="application/json")