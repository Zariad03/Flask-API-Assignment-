from flask import Flask, jsonify, request
import unittest

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello():
    name = request.args.get("name", "Zaria").strip()
    if not name:
        name = "Zaria"
    return jsonify({"message": f"Hello, {name}!"}), 200


@app.route("/sum", methods=["POST"])
def calculate_sum():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    if "numbers" not in data:
        return jsonify({"error": "Please provide a numbers list."}), 400

    numbers = data["numbers"]

    if not isinstance(numbers, list):
        return jsonify({"error": "Numbers must be a list."}), 400

    if any(isinstance(n, bool) or not isinstance(n, (int, float)) for n in numbers):
        return jsonify({"error": "Numbers must contain numbers only."}), 400

    return jsonify({"sum": sum(numbers)}), 200


class FlaskAPITests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_default(self):
        r = self.client.get("/hello")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"message": "Hello, Zaria!"})

    def test_hello_custom(self):
        r = self.client.get("/hello?name=John")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"message": "Hello, John!"})

    def test_hello_blank(self):
        r = self.client.get("/hello?name=")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"message": "Hello, Zaria!"})

    def test_sum_integers(self):
        r = self.client.post("/sum", json={"numbers": [1, 2, 3]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"sum": 6})

    def test_sum_decimals(self):
        r = self.client.post("/sum", json={"numbers": [1.5, 2.5]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"sum": 4.0})

    def test_sum_negative(self):
        r = self.client.post("/sum", json={"numbers": [-2, 5]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"sum": 3})

    def test_sum_empty(self):
        r = self.client.post("/sum", json={"numbers": []})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"sum": 0})

    def test_missing_numbers(self):
        r = self.client.post("/sum", json={})
        self.assertEqual(r.status_code, 400)

    def test_numbers_not_list(self):
        r = self.client.post("/sum", json={"numbers": 123})
        self.assertEqual(r.status_code, 400)

    def test_text_in_numbers(self):
        r = self.client.post("/sum", json={"numbers": [1, "hello"]})
        self.assertEqual(r.status_code, 400)

    def test_boolean_in_numbers(self):
        r = self.client.post("/sum", json={"numbers": [1, True]})
        self.assertEqual(r.status_code, 400)

    def test_invalid_json(self):
        r = self.client.post("/sum", data="invalid", content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_json_array(self):
        r = self.client.post("/sum", json=[1, 2, 3])
        self.assertEqual(r.status_code, 400)

    def test_wrong_method(self):
        r = self.client.get("/sum")
        self.assertEqual(r.status_code, 405)


suite = unittest.TestLoader().loadTestsFromTestCase(FlaskAPITests)
result = unittest.TextTestRunner(verbosity=2).run(suite)

if not result.wasSuccessful():
    raise SystemExit(1)
