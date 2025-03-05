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
from torch import clamp

parser = argparse.ArgumentParser()
parser.add_argument("--comfy-tag", type=str)
parser.add_argument("--mgr-tag", type=str)
parser.add_argument("--model-name", type=str, default="")
parser.add_argument("--positive-prompt", type=str, default="")
parser.add_argument("--negative-prompt", type=str, default="")
parser.add_argument("--width", type=int, default=0)
parser.add_argument("--height", type=int, default=0)
parser.add_argument("--length", type=int, default=0)
parser.add_argument("--input-img-name", type=str, default="")
parser.add_argument("--seed", type=int, default=0)
parser.add_argument("--steps", type=int, default=0)
parser.add_argument("--cfg", type=float, default=0)
parser.add_argument("--denoise", type=float, default=0)
parser.add_argument("--output-frame-rate", type=int, default=0)
parser.add_argument("--terminate-colab", action="store_true")
parser.add_argument("--run-step", type=int, default=0)
args = parser.parse_args()

comfy_tag: str = args.comfy_tag
mgr_tag: str = args.mgr_tag
model_name: str = args.model_name
positive_prompt: str = args.positive_prompt
negative_prompt: str = args.negative_prompt
width: int = args.width
height: int = args.height
length: int = args.length
input_img_name: str = args.input_img_name
seed: int = args.seed if args.seed >= 0 else np.random.randint(0, 2000000000)
steps: int = args.steps
cfg: float = args.cfg
denoise: float = args.denoise
output_frame_rate: int = args.output_frame_rate
terminate_colab_enabled: bool = args.terminate_colab
run_step:int = args.run_step

if (length - 1) % 4 != 0:
    for diff in range(1, 4):
        if ((length + diff) - 1) % 4 == 0:
            length = length + diff
            break


base_dir = "/content/drive/MyDrive/comfy_donato_wan"
input_dir = os.path.join(base_dir, "input")
input_img_path = os.path.join(input_dir, input_img_name)
output_dir = os.path.join(base_dir, "output")
wf_renderer_path = os.path.join(base_dir, "workflow_donato_wan_api.json")

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

def get_my_timestr() -> str:
    return datetime.today().strftime("%Y-%m-%d_%H-%M-%S")

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

def queue_render(loop_index: int, time_prefix: str):
    with open(wf_renderer_path, "rt", encoding="UTF8") as json_file:
        prompt = json.load(json_file)

    try:
        node_sampler = prompt["3"]["inputs"]
        node_sampler["seed"] = seed
        node_sampler["steps"] = steps
        node_sampler["cfg"] = cfg
        node_sampler["denoise"] = denoise

        node_positive = prompt["6"]["inputs"]
        node_positive["text"] = positive_prompt

        node_negative = prompt["7"]["inputs"]
        node_negative["text"] = negative_prompt

        node_model_loader = prompt["37"]["inputs"]
        node_model_loader["unet_name"] = model_name

        node_video = prompt["54"]["inputs"]
        node_video["frame_rate"] = output_frame_rate
        node_video["filename_prefix"] = f"donato_wan_{time_prefix}"

        node_input = prompt["55"]["inputs"]
        node_input["image"] = input_img_path

        node_width = prompt["56"]["inputs"]
        node_width["value"] = width

        node_height = prompt["57"]["inputs"]
        node_height["value"] = height

        node_length = prompt["58"]["inputs"]
        node_length["value"] = length

        node_img_out = prompt["59"]["inputs"]
        node_img_out["filename_prefix"] = "img"
        node_img_out["subfolder_dir"] = f"out_frames_{time_prefix}"

        queue_and_wait_prompt(prompt)

    except Exception as e:
        raise e


LOCAL_COMFY_BASE_DIR = "/usr/local/comfy"
LOCAL_COMFY_DIR = os.path.join(LOCAL_COMFY_BASE_DIR, "ComfyUI")
CUSTOM_NODES_DIR = os.path.join(LOCAL_COMFY_DIR, "custom_nodes")

def clone_custom_node(owner_name: str, repo_name: str, co_name: str):
    os.chdir(CUSTOM_NODES_DIR)
    os.system(f"git clone --recursive https://github.com/{owner_name}/{repo_name}.git")
    os.chdir(os.path.join(CUSTOM_NODES_DIR, repo_name))
    os.system(f"git checkout {co_name}")
    os.chdir(CUSTOM_NODES_DIR)

def download(target:str, local_dir:str, threads:int, repo:str="DonatoDiffusion/trytonado"):
    url = f"https://huggingface.co/{repo}/resolve/main/{target}"
    file = os.path.basename(url)
    os.system(f"aria2c -c {url} -o {file} --console-log-level=error --file-allocation=none -x {threads} -s {threads} -k 50M -d {local_dir}")

if run_step == 1:
    os.system(f"mkdir -p {LOCAL_COMFY_BASE_DIR}")
    os.chdir(LOCAL_COMFY_BASE_DIR)
    os.system(f"git clone -b {comfy_tag} https://github.com/comfyanonymous/ComfyUI.git")
    os.chdir(LOCAL_COMFY_DIR)
    os.system("pip install xformers!=0.0.18 -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121")
    os.system("pip install diffusers timm==1.0.9 addict yapf open-clip-torch python-dotenv clip-interrogator insightface onnxruntime rembg piexif aria2 ultralytics deepdiff evalidate surrealist simpleeval pynvml boto3 segment_anything redis fal_client gitpython triton replicate dghs-imgutils[gpu] sageattention decord bitsandbytes llama-cpp-python dill")

    os.chdir(CUSTOM_NODES_DIR)
    os.system("git lfs install")
    os.system(f"git clone --recursive -b {mgr_tag} https://github.com/ltdrdata/ComfyUI-Manager.git")
    os.system("git clone --recursive -b 8.8.1 https://github.com/ltdrdata/ComfyUI-Impact-Pack.git")
    os.system("git clone --recursive -b 1.2.9 https://github.com/ltdrdata/ComfyUI-Impact-Subpack.git")
    os.system("git clone --recursive -b 1.13 https://github.com/ltdrdata/ComfyUI-Inspire-Pack.git")
    os.system("git clone --recursive -b v1.2.7 https://github.com/yolain/ComfyUI-Easy-Use.git")
    clone_custom_node("Kosinkadink", "ComfyUI-VideoHelperSuite", "4c7858ddd5126f7293dc3c9f6e0fc4c263cde079")
    clone_custom_node("melMass", "comfy_mtb", "d87e52ea2c112fd95f257dcd6a54a5db77a34fc3")
    clone_custom_node("kijai", "ComfyUI-KJNodes", "97d20e27e589854451a9d1f091f6524e947d6229")
    clone_custom_node("aria1th", "ComfyUI-LogicUtils", "2451f43fa7322b2d82cf61e74c51bb202acaa85c")

    os.chdir(os.path.join(LOCAL_COMFY_DIR, "models"))
    os.system("git lfs install")
    download("split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", "./text_encoders/", 16, "Comfy-Org/Wan_2.1_ComfyUI_repackaged")
    download("split_files/diffusion_models/wan2.1_i2v_720p_14B_bf16.safetensors", "./diffusion_models/", 16, "Comfy-Org/Wan_2.1_ComfyUI_repackaged")
    download("split_files/diffusion_models/wan2.1_t2v_14B_bf16.safetensors", "./diffusion_models/", 16, "Comfy-Org/Wan_2.1_ComfyUI_repackaged")
    download("split_files/vae/wan_2.1_vae.safetensors", "./vae/", 16, "Comfy-Org/Wan_2.1_ComfyUI_repackaged")
    download("split_files/clip_vision/clip_vision_h.safetensors", "./clip_vision/", 16, "Comfy-Org/Wan_2.1_ComfyUI_repackaged")

    try:
        os.chdir(LOCAL_COMFY_DIR)
        os.system(f"nohup python main.py --dont-print-server --input-directory {input_dir} --output-directory {output_dir} &")
    except Exception as e:
        print(f"X except: {str(e)}")
        raise e

if run_step == 2:
    try:
        prefix = get_my_timestr()
        queue_render(0, prefix)
        preview_path = os.path.join(LOCAL_COMFY_BASE_DIR, "preview.mp4")
        if os.path.isfile(preview_path):
            os.remove(preview_path)
        for f in glob.glob(os.path.join(output_dir, f"donato_wan_{prefix}*.mp4")):
            if os.path.isfile(f):
                shutil.copy(f, preview_path)
                break
        for f in glob.glob(os.path.join(output_dir, f"donato_wan_{prefix}*.png")):
            if os.path.isfile(f):
                os.remove(f)
                break
    except Exception as e:
        print(f"except: {str(e)}")
    if terminate_colab_enabled:
        terminate_colab()
