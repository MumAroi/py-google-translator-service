from flask import Flask, request, jsonify

from deep_translator import (GoogleTranslator)
# import language_tool_python

app = Flask(__name__)

PRIVATE_KEY="I3X23IxqxDOazSabbDVUte5IK1bGCVxr8GHO2Iyq9F4kTtBxF3VrVCpMMXxgQdGYU"

@app.route("/", methods=["POST"])
def translate():
    headers = request.headers
    bearer = headers.get('Authorization') 
    if bearer:
        token = bearer.split()[1]
        source = "thai"
        target = "english"
        if token != PRIVATE_KEY:
            return jsonify({"message": "Unauthorize"}), 403
            
        data = request.json
        if not data or "message" not in data:
            return jsonify({"message": "Not have message"}), 400

        if "source" in data:
            source = data["source"]

        if "target" in data:
            target = data["target"]

        text = data["message"]
        translated = GoogleTranslator(source=source, target=target).translate(text=text)
        # tool = language_tool_python.LanguageToolPublicAPI("en-US")
        
        return jsonify({
            "text": translated,
            # "text": tool.correct(translated)
        }), 200

    else:
        return jsonify({"message": "Unauthorize"}), 403


@app.route("/lang-support", methods=["GET"])
def langSupport():
    headers = request.headers
    bearer = headers.get('Authorization') 
    if bearer:
        token = bearer.split()[1]
        if token != PRIVATE_KEY:
            return jsonify({"message": "Unauthorize"}), 403
            
        langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

        return jsonify({
            "languages": langs_dict,
        }), 200

    else:
        return jsonify({"message": "Unauthorize"}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0')