from flask import Flask, request, jsonify

from deep_translator import (GoogleTranslator)
import language_tool_python

app = Flask(__name__)

PRIVATE_KEY="1223334444"

@app.route("/", methods=["POST"])
def translate():
    headers = request.headers
    bearer = headers.get('Authorization') 
    if bearer:
        token = bearer.split()[1]
        if token != PRIVATE_KEY:
            return jsonify({"message": "Unauthorize"}), 403
            
        data = request.json
        if not data or "message" not in data:
            return jsonify({"message": "Not have message"}), 400

        # text = 'ฟีเจอร์การถอดความทำงานด้วยการประเมินทั้งประโยคขณะที่เสียงยังดำเนินต่อไป จากตรงนั้นก็จะมีการใส่เครื่องหมายวรรคตอน เลือกสรรคำตามบริบทของประโยค และพยายามแก้สำเนียงและภาษาถิ่น ผู้ใช้งานก็น่าจะได้บทถอดแปลที่ค่อนข้างแม่นยำ ซึ่งบริษัทก็คาดว่าโมเดล AI น่าจะช่วยพัฒนาขึ้นเรื่อยๆ เมื่อเวลาผ่านไป'
        text = data["message"]
        translated = GoogleTranslator(source="th", target="en").translate(text=text)
        tool = language_tool_python.LanguageToolPublicAPI("en-US")
        
        return jsonify({
            "text": tool.correct(translated)
        }), 200

    else:
        return jsonify({"message": "Unauthorize"}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0')