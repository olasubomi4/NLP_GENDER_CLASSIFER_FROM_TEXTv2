import joblib
class Encoder:
    def __init__(self, encoder):
        self.encoder=encoder

    def encode(self,text:str)->str:
        encoded_text=self.encoder.encode(text);
        encoded_text=encoded_text.reshape(1,-1);
        return encoded_text;

