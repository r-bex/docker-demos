from flask import Flask, jsonify, request

app = Flask(__name__)

class AnimalPredictor():
    def predict(self, input_features):
        legs = input_features.get('legs', 2)
        if legs > 4:
            return "insect"
        elif legs == 4:
            return "dog"
        elif legs == 2:
            return "human"
        else:
            return "unknown"

def load_model():
    return AnimalPredictor()

# -- below here = routing for app --

@app.route("/predict", methods=["POST"])
def predict():
    model_input = request.get_json()
    model = load_model()
    return jsonify({"prediction": model.predict(model_input)})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
