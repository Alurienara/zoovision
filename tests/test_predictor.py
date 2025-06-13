from model.predictor import predict_image
from PIL import Image
import os


def test_predict_image_output_format():
    img_path = os.path.join("tests", "sample.jpg")
    img = Image.new(
        "RGB", (224, 224), color="white"
    )  # простое белое изображение
    results = predict_image(img)
    assert isinstance(results, list)
    assert all(
        isinstance(label, str) and isinstance(prob, float)
        for label, prob in results
    )
