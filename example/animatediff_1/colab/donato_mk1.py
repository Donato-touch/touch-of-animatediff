import json
import urllib.request
import urllib.parse
import uuid
import websocket
import os
import stat
import time
import json
import sys
import glob
import shutil
import subprocess
import math
import numpy as np
from datetime import datetime
import argparse
from google.colab import drive, runtime

parser = argparse.ArgumentParser()
parser.add_argument("--comfy-tag", type=str)
parser.add_argument("--mgr-tag", type=str)
parser.add_argument("--ckpt-name", type=str)
parser.add_argument("--vae-name", type=str)
parser.add_argument("--positive-prompt", type=str)
parser.add_argument("--negative-prompt", type=str)
args = parser.parse_args()

comfy_tag: str = args.comfy_tag
mgr_tag: str = args.mgr_tag
ckpt_name = args.ckpt_name
vae_name = args.vae_name
positive_prompt = args.positive_prompt
negative_prompt = args.negative_prompt

if ckpt_name == "":
    ckpt_name = "meinamix_meinaV11.safetensors"
if vae_name == "":
    vae_name = "vae-ft-mse-840000-ema-pruned.ckpt"

cur_seed = np.random.randint(0, 2000000000)
batch_size = 150
input_dir = "/content/drive/MyDrive/comfy_donato/input"
input_video_path = os.path.join(input_dir, "input_video.mp4")
output_dir = "/content/drive/MyDrive/comfy_donato/output"
output_frame_dir = os.path.join(output_dir, "detailed_out")
wf_renderer_path = "/content/drive/MyDrive/comfy_donato/workflow_renderer_api.json"
wf_video_maker_path = "/content/drive/MyDrive/comfy_donato/workflow_video_maker_api.json"

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def terminate_colab():
    print(" ===== TERMINATE COLAB =====")
    time.sleep(10)
    drive.flush_and_unmount()
    runtime.unassign()
    print(" ===== TERMINATE COLAB =====")

def del_ro_dir(dir_name):
	for (root, dirs, files) in os.walk(dir_name, topdown=True):
		os.chmod(root,
			# For user ...
			stat.S_IRUSR |
			stat.S_IWUSR |
			stat.S_IXUSR |
			# For group ...
			stat.S_IWGRP |
			stat.S_IRGRP |
			stat.S_IXGRP |
			# For other ...
			stat.S_IROTH |
			stat.S_IWOTH |
			stat.S_IXOTH
		)
	shutil.rmtree(dir_name, ignore_errors=True)

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    res = json.loads(urllib.request.urlopen(req).read())
    return res["prompt_id"]

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        res = json.loads(response.read())
        return res

def queue_and_wait_prompt(prompt):
    ws = websocket.WebSocket()
    for i in range(0, 11):
        if i >= 10:
            ws = websocket.WebSocket()
            ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
        else:
            try:
                ws = websocket.WebSocket()
                ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
            except:
                print(f"wait and retry ws connection... ({i})")
                time.sleep(30)
                continue
        break
    ws.close()
    ws = None
    prompt_id = queue_prompt(prompt)
    while True:
        history = get_history(prompt_id)
        try:
            completed = history[prompt_id]["status"]["completed"]
            if completed:
                print(f"prompt completed, {prompt_id}")
                break
            else:
                print("===process failed!!!")
                raise Exception("reraise", "===process failed!!!")
        except Exception as e:
            if len(e.args) >= 1 and e.args[0] == "reraise":
                raise
            else:
                time.sleep(5)
        else:
            time.sleep(5)

def queue_render(loop_index: int):
    with open(wf_renderer_path, "rt", encoding="UTF8") as json_file:
        prompt = json.load(json_file)

    try:
        node_input_video = prompt["1"]["inputs"]
        node_input_video["video"] = input_video_path

        node_ckpt = prompt["2"]["inputs"]
        node_ckpt["ckpt_name"] = ckpt_name

        node_vae = prompt["3"]["inputs"]
        node_vae["vae_name"] = vae_name

        node_batch_size = prompt["6"]["inputs"]
        node_batch_size["value"] = batch_size

        node_positive = prompt["9"]["inputs"]
        node_positive["text"] = positive_prompt

        node_negative = prompt["11"]["inputs"]
        node_negative["text"] = negative_prompt

        node_seed = prompt["22"]["inputs"]
        node_seed["value"] = cur_seed

        node_loop_index = prompt["34"]["inputs"]
        node_loop_index["seed"] = loop_index

        queue_and_wait_prompt(prompt)

    except Exception as e:
        raise e

def queue_video():
    with open(wf_video_maker_path, "rt", encoding="UTF8") as json_file:
        prompt = json.load(json_file)

    try:
        node_input_video = prompt["1"]["inputs"]
        node_input_video["video"] = input_video_path

        node_input_frames = prompt["2"]["inputs"]
        node_input_frames["directory"] = output_frame_dir

        queue_and_wait_prompt(prompt)

    except Exception as e:
        raise e

LOCAL_COMFY_BASE_DIR = "/usr/local/comfy"
LOCAL_COMFY_DIR = os.path.join(LOCAL_COMFY_BASE_DIR, "ComfyUI")
CUSTOM_NODES_DIR = os.path.join(LOCAL_COMFY_DIR, "custom_nodes")

os.system(f"mkdir -p {LOCAL_COMFY_BASE_DIR}")
os.chdir(LOCAL_COMFY_BASE_DIR)
os.system(f"git clone -b {comfy_tag} https://github.com/comfyanonymous/ComfyUI.git")
os.chdir(LOCAL_COMFY_DIR)
os.system("pip install xformers!=0.0.18 -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121")
os.system("pip install diffusers timm==1.0.9 addict yapf open-clip-torch python-dotenv clip-interrogator insightface onnxruntime rembg piexif aria2 ultralytics deepdiff evalidate surrealist simpleeval pynvml boto3 segment_anything redis fal_client gitpython triton replicate dghs-imgutils[gpu] sageattention decord bitsandbytes llama-cpp-python")

def clone_custom_node(owner_name: str, repo_name: str, co_name: str):
    os.chdir(CUSTOM_NODES_DIR)
    os.system(f"git clone --recursive https://github.com/{owner_name}/{repo_name}.git")
    os.chdir(os.path.join(CUSTOM_NODES_DIR, repo_name))
    os.system(f"git checkout {co_name}")
    os.chdir(CUSTOM_NODES_DIR)

os.chdir(CUSTOM_NODES_DIR)
os.system("git lfs install")
os.system(f"git clone --recursive -b {mgr_tag} https://github.com/ltdrdata/ComfyUI-Manager.git")
os.system("git clone --recursive -b 8.0.1 https://github.com/ltdrdata/ComfyUI-Impact-Pack.git")
os.system("git clone --recursive -b 1.1 https://github.com/ltdrdata/ComfyUI-Impact-Subpack.git")
os.system("git clone --recursive -b 1.9 https://github.com/ltdrdata/ComfyUI-Inspire-Pack.git")
clone_custom_node("Suzie1", "ComfyUI_Comfyroll_CustomNodes", "d78b780")
clone_custom_node("Fannovel16", "comfyui_controlnet_aux", "5a049bd")
clone_custom_node("Fannovel16", "ComfyUI-Frame-Interpolation", "c336f71")
clone_custom_node("Kosinkadink", "ComfyUI-Advanced-ControlNet", "9632af9")
clone_custom_node("Kosinkadink", "ComfyUI-AnimateDiff-Evolved", "4f1344e")
clone_custom_node("Kosinkadink", "ComfyUI-VideoHelperSuite", "78753db")
clone_custom_node("cubiq", "ComfyUI_IPAdapter_plus", "b188a6c")
clone_custom_node("cubiq", "ComfyUI_essentials", "33ff89f")
clone_custom_node("pythongosssss", "ComfyUI-Custom-Scripts", "19a82e2")
clone_custom_node("jags111", "efficiency-nodes-comfyui", "3ead4af")
clone_custom_node("BadCafeCode", "masquerade-nodes-comfyui", "432cb4d")
clone_custom_node("melMass", "comfy_mtb", "827c64c")
clone_custom_node("FizzleDorf", "ComfyUI_FizzNodes", "7d6ea60")
clone_custom_node("alt-key-project", "comfyui-dream-project", "b5c804a")
clone_custom_node("kijai", "ComfyUI-KJNodes", "973ceb6")
clone_custom_node("kijai", "ComfyUI-Florence2", "27714ba")
clone_custom_node("kijai", "ComfyUI-Marigold", "1894ff2")
clone_custom_node("kijai", "ComfyUI-HunyuanVideoWrapper", "46e31f1")
clone_custom_node("WASasquatch", "was-node-suite-comfyui", "fe7e088")
clone_custom_node("sipherxyz", "comfyui-art-venture", "50abaac")
clone_custom_node("rgthree", "rgthree-comfy", "5f2d8a1")
clone_custom_node("chrisgoringe", "cg-image-picker", "aaab0d3")
clone_custom_node("crystian", "ComfyUI-Crystools", "03a61d6")
clone_custom_node("TheBill2001", "comfyui-upscale-by-model", "f8bb900")
clone_custom_node("TinyTerra", "ComfyUI_tinyterraNodes", "339ee9c")
clone_custom_node("ssitu", "ComfyUI_UltimateSDUpscale", "e617ff2")
clone_custom_node("evanspearman", "ComfyMath", "939bb81")
clone_custom_node("jamesWalker55", "comfyui-various", "36454f9")
clone_custom_node("bash-j", "mikey_nodes", "637bc18")
clone_custom_node("SuperBeastsAI", "ComfyUI-SuperBeasts", "f684c86")
clone_custom_node("storyicon", "comfyui_segment_anything", "ab63955")
clone_custom_node("aria1th", "ComfyUI-LogicUtils", "eb3a0d0")
clone_custom_node("XLabs-AI", "x-flux-comfyui", "0032855")
clone_custom_node("Lightricks", "ComfyUI-LTXVideo", "8cbf26c")
clone_custom_node("IuvenisSapiens", "ComfyUI_MiniCPM-V-2_6-int4", "ed210d8")
os.system(f"mkdir {os.path.join(LOCAL_COMFY_DIR, 'models', 'LLM')}")

def download(target:str, local_dir:str, threads:int, repo:str="DonatoDiffusion/trytonado"):
    url = f"https://huggingface.co/{repo}/resolve/main/{target}"
    file = os.path.basename(url)
    os.system(f"aria2c -c {url} -o {file} --console-log-level=error --file-allocation=none -x {threads} -s {threads} -k 50M -d {local_dir}")

os.chdir(os.path.join(LOCAL_COMFY_DIR, "models"))
os.system("git lfs install")
os.system('huggingface-cli download DonatoDiffusion/trytonado --include "ultralytics/*" --local-dir ./')
download("sd15/animatediff_models/motionModel_v03anime.ckpt", "./animatediff_models/", 16)
download("sd15/controlnet/control_v11f1e_sd15_tile.pth", "./controlnet/", 16)
download("sd15/controlnet/control_v11p_sd15_openpose.pth", "./controlnet/", 16)
download("sd15/controlnet/control_v11f1e_sd15_tile.yaml", "./controlnet/", 1)
download("sd15/controlnet/control_v11p_sd15_openpose.yaml", "./controlnet/", 1)
download("loras/LCM_LoRA_Weights_SD15.safetensors", "./loras/", 1)
download("upscale_models/4xUltrasharp_4xUltrasharpV10.pth", "./upscale_models/", 1)

if ckpt_name == "meinamix_meinaV11.safetensors":
    download("sd15/checkpoints/meinamix_meinaV11.safetensors", "./checkpoints/", 16)
else:
    shutil.copy(os.path.join(input_dir, ckpt_name), os.path.join(LOCAL_COMFY_DIR, "models", "checkpoints", ckpt_name))
if vae_name == "vae-ft-mse-840000-ema-pruned.ckpt":
    download("sd15/vae/vae-ft-mse-840000-ema-pruned.ckpt", "./vae/", 16)
else:
    shutil.copy(os.path.join(input_dir, vae_name), os.path.join(LOCAL_COMFY_DIR, "models", "vae", vae_name))

try:
    os.chdir(LOCAL_COMFY_DIR)
    os.system(f"python main.py --dont-print-server --input-directory {input_dir} --output-directory {output_dir} &")
except Exception as e:
    print(f"X except: {str(e)}")
    terminate_colab()
    raise e

del_ro_dir(output_frame_dir)
time.sleep(60)

loop_i = 0
while True:
    try:
        queue_render(loop_i)
    except Exception as e:
        print(f"except: {str(e)}")
        try:
            queue_video()
        except:
            pass
        terminate_colab()
    loop_i += 1
