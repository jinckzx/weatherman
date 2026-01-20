import os
import pickle
from huggingface_hub import hf_hub_download

HF_REPO_ID = "anmolsehgal/weatherman"  # CHANGE THIS

MODEL_MAP = {
    ("temperature", "delhi"): "temp_delhi.pkl",
    ("temperature", "kolkata"): "temp_kolkata.pkl",
    ("humidity", "delhi"): "rhum_delhi.pkl",
    ("humidity", "kolkata"): "rhum_kolkata.pkl",
}

MODELS = {}

def load_models():
    for key, filename in MODEL_MAP.items():
        model_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=filename
        )
        with open(model_path, "rb") as f:
            MODELS[key] = pickle.load(f)

# Load models at import time
load_models()
