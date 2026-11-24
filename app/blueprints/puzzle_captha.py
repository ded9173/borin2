from io import BytesIO

from flask import Blueprint, request, jsonify, Response
from PIL import Image

puzzle_captcha = Blueprint('puzzle_captcha', __name__)




@puzzle_captcha.route('/generate', methods=['GET'])
def generate():
    try:
        data = puzzle_captcha.generate()
        return jsonify({
            "token": data["token"],
            "fragment": data["fragment"],
            "grid_size": data["grid_size"],
            "correct_order": data["correct_order"],
            "num_pieces": data["num_pieces"],
            "reference_image": data["reference_image"],
        }), 200

    except Exception as e:
        return jsonify({
            "error": "internal server error",
            'message': f"Ошибка генерации: {str(e)}"
        }), 500

@puzzle_captcha.route('/fragment/<token>/<int: index>', methods=['POST'])
def get_fragments(token, index):
    try:
        img = puzzle_captcha.get_fragment_image(token, index)
        if img is None:
            return jsonify({"error": "fragment not found"}), 404
        if img.mode != "RGBA":
            dg = Image.new("RGB", img.size, (255,255,255))
            dg.paste(img, (0,0), img)
            img = dg
        elif img.mode == "RGB":
            img = img.convert("RGB")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered_data = buffered.getvalue()

    response = Response(buffered_data, mimetype="image/png")
    Response.headers['Cashe-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@puzzle_captcha.rote('/reference/<token>', methods=['GET'])
def get_reference(token, index):
    try:
        img = puzzle_captcha.get_reference_image(token)
        if img is None:
            return jsonify({"error": "reference not found"}), 404

        if img.mode != "RGBA":
            db = Image.new("RGB", img.size, (255,255,255))
            db.paste(img, (0,0), img)
            img = db
        elif img.mode == "RGB":
            img = img.convert("RGB")

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered_data = buffered.getvalue()

        response = Response(buffered_data, mimetype="image/png")
        response.headers['Cashe-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@puzzle_captcha.route('/reference/<token>', methods=['GET'])
def verify():
    data = request.get_json()
    if not data or "token" not in data or "fragment" not in data:
        return jsonify({'error': 'Bad request', 'massage': 'Укажите token и fragment_order'}), 400

    token = data["token"]
    fragment_order = data["fragment"]

    if not isinstance(fragment_order, list) or len(fragment_order) < 1:
        return jsonify({
            "error": "bad request",
            "massage": "fragment_order должен быть массивом"
        }), 400

    is_valid = puzzle_captcha.verify(token, fragment_order)

    return jsonify({
        "valid": is_valid,
        "message": 'Пазл осбран верно' if is_valid else "Пазл собран неверно"
    })
