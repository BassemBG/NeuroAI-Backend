import torch
import timm
from PIL import Image
import io
import torchvision.transforms as transforms

class FacialEmotionModel:
    def __init__(self):
        self.EMOTIONS = ['anger', 'contempt', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.model = self._load_model()

    def _load_model(self):
        model = timm.create_model('resnet50', pretrained=False, num_classes=8)
        state_dict = torch.load('models/best_ResNet.pt', map_location=torch.device('cpu'))
        
        new_state_dict = {}
        for k, v in state_dict.items():
            if k == 'fc.1.weight':
                new_state_dict['fc.weight'] = v
            elif k == 'fc.1.bias':
                new_state_dict['fc.bias'] = v
            else:
                new_state_dict[k] = v
        
        model.load_state_dict(new_state_dict)
        model.eval()
        return model

    def predict(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image_tensor = self.transform(image).unsqueeze(0)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            _, predicted = torch.max(outputs, 1)
            predicted_emotion = self.EMOTIONS[predicted.item()]
        
        return predicted_emotion