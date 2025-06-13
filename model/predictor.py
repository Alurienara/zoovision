import torch
from torchvision import models, transforms
from PIL import Image
import os

# Путь к модели
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'weights', 'resnet50-0676ba61.pth')

# Создание модели
model = models.resnet50()
state_dict = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
model.load_state_dict(state_dict)
model.eval()

# Классы ImageNet
LABELS_URL = 'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt'
import urllib.request
with urllib.request.urlopen(LABELS_URL) as f:
    categories = [line.strip().decode("utf-8") for line in f]

# Предобработка
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

def predict_image(image: Image.Image):
    input_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
    probs = torch.nn.functional.softmax(output[0], dim=0)
    top5 = torch.topk(probs, 5)
    results = [(categories[i], probs[i].item()) for i in top5.indices]
    return results
