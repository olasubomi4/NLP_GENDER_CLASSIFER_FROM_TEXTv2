from service import EncoderService
import joblib

class PredictorService:
    def __init__(self,encoderService:EncoderService,ml_model):
        self.encoderService = encoderService
        self.mlModel = ml_model

    def predict(self, text):
        encoded_text = self.encoderService.encode(text)
        ml_prediction = self.mlModel.predict(encoded_text)
        if(ml_prediction == 1):
            return "Male"
        return "Female"

    def predict2(self, text):
        encoded_text = self.encoderService.encode(text)
        ml_prediction = self.mlModel.predict(encoded_text)

        result=[{"Blog text":text[i], "Gender:":"Male"} if ml_prediction[i]==1  else {"Blog text":text[i], "Gender:":"Male"}  for i in range(len(text))]
        return result

        # for i in range(len(text)):
        #     result[text[i]]=if(ml_prediction[i]==1):"Male" else "Female"
        #
        # return result
        # if(ml_prediction == 1):
        #     return "Male"
        # return "Female"