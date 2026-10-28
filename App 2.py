from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello():
    name = request.args.get("name", "Zaria").strip()

    if not name:
        name = "Zaria"

    return jsonify({"message": f"Hello, {name}!"})


@app.route("/sum", methods=["POST"])
def calculate_sum():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    numbers = data.get("numbers")

    if not isinstance(numbers, list):
        return jsonify({"error": "Numbers must be provided as a list."}), 400

    if any(isinstance(n, bool) or not isinstance(n, (int, float)) for n in numbers):
        return jsonify({"error": "Numbers must contain numbers only."}), 400

    return jsonify({"sum": sum(numbers)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

import unittest
from app import app


class FlaskAPITests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_default(self):
        response = self.client.get("/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, Zaria!"})

    def test_hello_custom_name(self):
        response = self.client.get("/hello?name=John")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, John!"})

    def test_hello_blank_name(self):
        response = self.client.get("/hello?name=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, Zaria!"})

    def test_sum_integers(self):
        response = self.client.post("/sum", json={"numbers": [1, 2, 3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 6})

    def test_sum_decimals(self):
        response = self.client.post("/sum", json={"numbers": [1.5, 2.5]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 4.0})

    def test_sum_negative_numbers(self):
        response = self.client.post("/sum", json={"numbers": [-2, 5]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 3})

    def test_sum_empty_list(self):
        response = self.client.post("/sum", json={"numbers": []})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 0})

    def test_missing_numbers(self):
        response = self.client.post("/sum", json={})
        self.assertEqual(response.status_code, 400)

    def test_numbers_not_list(self):
        response = self.client.post("/sum", json={"numbers": 123})
        self.assertEqual(response.status_code, 400)

    def test_text_in_numbers(self):
        response = self.client.post("/sum", json={"numbers": [1, "hello", 3]})
        self.assertEqual(response.status_code, 400)

    def test_boolean_in_numbers(self):
        response = self.client.post("/sum", json={"numbers": [1, True, 3]})
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(
            "/sum", data="not valid JSON", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_json_array_instead_of_object(self):
        response = self.client.post("/sum", json=[1, 2, 3])
        self.assertEqual(response.status_code, 400)

    def test_wrong_http_method(self):
        response = self.client.get("/sum")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main(verbosity=2)

import unittest
from app import app


class FlaskAPITests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_default(self):
        response = self.client.get("/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, Zaria!"})

    def test_hello_custom_name(self):
        response = self.client.get("/hello?name=John")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, John!"})

    def test_hello_blank_name(self):
        response = self.client.get("/hello?name=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, Zaria!"})

    def test_sum_integers(self):
        response = self.client.post("/sum", json={"numbers": [1, 2, 3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 6})

    def test_sum_decimals(self):
        response = self.client.post("/sum", json={"numbers": [1.5, 2.5]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 4.0})

    def test_sum_negative_numbers(self):
        response = self.client.post("/sum", json={"numbers": [-2, 5]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 3})

    def test_sum_empty_list(self):
        response = self.client.post("/sum", json={"numbers": []})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 0})

    def test_missing_numbers(self):
        response = self.client.post("/sum", json={})
        self.assertEqual(response.status_code, 400)

    def test_numbers_not_list(self):
        response = self.client.post("/sum", json={"numbers": 123})
        self.assertEqual(response.status_code, 400)

    def test_text_in_numbers(self):
        response = self.client.post("/sum", json={"numbers": [1, "hello", 3]})
        self.assertEqual(response.status_code, 400)

    def test_boolean_in_numbers(self):
        response = self.client.post("/sum", json={"numbers": [1, True, 3]})
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(
            "/sum", data="not valid JSON", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_json_array_instead_of_object(self):
        response = self.client.post("/sum", json=[1, 2, 3])
        self.assertEqual(response.status_code, 400)

    def test_wrong_http_method(self):
        response = self.client.get("/sum")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main(verbosity=2)

import unittest
from app import app


class FlaskAPITests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_default(self):
        response = self.client.get("/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, Zaria!"})

    def test_hello_custom_name(self):
        response = self.client.get("/hello?name=John")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, John!"})

    def test_hello_blank_name(self):
        response = self.client.get("/hello?name=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, Zaria!"})

    def test_sum_integers(self):
        response = self.client.post("/sum", json={"numbers": [1, 2, 3]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 6})

    def test_sum_decimals(self):
        response = self.client.post("/sum", json={"numbers": [1.5, 2.5]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 4.0})

    def test_sum_negative_numbers(self):
        response = self.client.post("/sum", json={"numbers": [-2, 5]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 3})

    def test_sum_empty_list(self):
        response = self.client.post("/sum", json={"numbers": []})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"sum": 0})

    def test_missing_numbers(self):
        response = self.client.post("/sum", json={})
        self.assertEqual(response.status_code, 400)

    def test_numbers_not_list(self):
        response = self.client.post("/sum", json={"numbers": 123})
        self.assertEqual(response.status_code, 400)

    def test_text_in_numbers(self):
        response = self.client.post("/sum", json={"numbers": [1, "hello", 3]})
        self.assertEqual(response.status_code, 400)

    def test_boolean_in_numbers(self):
        response = self.client.post("/sum", json={"numbers": [1, True, 3]})
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(
            "/sum", data="not valid JSON", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_json_array_instead_of_object(self):
        response = self.client.post("/sum", json=[1, 2, 3])
        self.assertEqual(response.status_code, 400)

    def test_wrong_http_method(self):
        response = self.client.get("/sum")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main(verbosity=2)
