import torch
import torch.nn as nn
from torchvision import models, transforms
import joblib
from PIL import Image
import cv2

# ---------------- Configuration ----------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMG_SIZE = 224

# ⚠️ MUST match training label order
CLASS_NAMES = ["FAKE", "REAL"]

# ---------------- Load Models (ONCE) ----------------
def load_models():
    mobilenet = models.mobilenet_v2(pretrained=True)
    mobilenet.classifier = nn.Identity()

    mobilenet.load_state_dict(
        torch.load(
            "models/mobilenet_feature_extractor_split.pth",
            map_location=DEVICE
        )
    )

    mobilenet.to(DEVICE)
    mobilenet.eval()

    svc = joblib.load("models/linear_svc_mobilenet_split.joblib")

    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    return mobilenet, svc, transform


mobilenet, svc, transform = load_models()

# ---------------- IMAGE PREDICTION ----------------
@torch.no_grad()
def predict_image(pil_img: Image.Image) -> str:
    pil_img = pil_img.convert("RGB")
    img = transform(pil_img).unsqueeze(0).to(DEVICE)

    features = mobilenet(img)
    features = features.cpu().numpy()

    pred = svc.predict(features)[0]
    return CLASS_NAMES[int(pred)]


# ---------------- VIDEO PREDICTION (ROBUST) ----------------
@torch.no_grad()
def predict_video(video_path, frame_skip=10, max_frames=150) -> str:
    cap = cv2.VideoCapture(video_path)

    preds = []
    frame_count = 0

    while cap.isOpened() and len(preds) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = rgb.shape
            s = min(h, w)

            # Center crop
            crop = rgb[
                (h - s)//2:(h + s)//2,
                (w - s)//2:(w + s)//2
            ]

            img = Image.fromarray(crop)
            pred = predict_image(img)
            preds.append(pred)

        frame_count += 1

    cap.release()

    # ---------- Safety check ----------
    if len(preds) < 20:
        return "UNKNOWN"

    fake_count = preds.count("FAKE")
    real_count = preds.count("REAL")
    total = len(preds)

    fake_ratio = fake_count / total

    # ---------- ROBUST DECISION RULE ----------
    # FAKE only if strong & consistent fake dominance
    if fake_ratio >= 0.7 and fake_count >= 30 and real_count <= total * 0.5:
        return "FAKE"
    else:
        return "REAL"
