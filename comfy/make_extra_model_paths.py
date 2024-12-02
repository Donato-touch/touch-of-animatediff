import yaml
import os

extra_paths = {
    "comfyui": {
        "base_path": os.getcwd(),
        "shared_models": "models/",
        "checkpoints": "models/checkpoints/",
        "configs": "models/configs/",
        "loras": "models/loras/",
        "vae": "models/vae/",
        "clip": "models/clip/",
        "unet": "models/unet/",
        "clip_vision": "models/clip_vision/",
        "style_models": "models/style_models/",
        "embeddings": "models/embeddings/",
        "diffusers": "models/diffusers/",
        "vae_approx": "models/vae_approx/",
        "controlnet": "models/controlnet/",
        "gilgen": "models/gilgen/",
        "upscale_models": "models/upscale_models/",
        "hypernetworks": "models/hypernetworks/",
        "photomaker": "models/photomaker/",
        "classifiers": "models/classifiers/",
        "animatediff_models": "models/animatediff_models/",
        "animatediff_motion_lora": "models/animatediff_motion_lora/",
        "insightface": "models/insightface/",
        "face_restore": "models/facerestore_models/",
        "facerestore_models": "models/facerestore_models/",
        "ipadapter": "models/ipadapter/",
        "sams": "models/sams/",
        "mmdets": "models/mmdets/",
        "ultralytics": "models/ultralytics/",
        "ultralytics_bbox": "models/ultralytics/bbox/",
        "ultralytics_segm": "models/ultralytics/segm/",
        "layer_model": "models/layer_model/",
        "grounding-dino": "models/grounding-dino/"
    }
}

with open("extra_model_paths.yaml", "wt", encoding="UTF8") as f:
    yaml.dump(extra_paths, f, default_flow_style=False, indent=4)
