import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--comfy-tag", type=str)
parser.add_argument("--mgr-tag", type=str)
parser.add_argument("--flux-enabled", action="store_true")
parser.add_argument("--flux-fp8-enabled", action="store_true")
parser.add_argument("--flux-controlnet", action="store_true")
parser.add_argument("--flux-controlnet-inpainting", action="store_true")
parser.add_argument("--flux-ipadapter", action="store_true")
parser.add_argument("--flux-turbo-alpha-lora", action="store_true")
parser.add_argument("--hunyuan-enabled", action="store_true")
parser.add_argument("--deepseek-enabled", action="store_true")
parser.add_argument("--sdxl-enabled", action="store_true")
parser.add_argument("--wan-enabled", action="store_true")
parser.add_argument("--wan-fun-enabled", action="store_true")
args = parser.parse_args()

comfy_tag: str = args.comfy_tag
mgr_tag: str = args.mgr_tag
flux_enabled: bool = args.flux_enabled
flux_fp8_enabled: bool = args.flux_fp8_enabled
flux_controlnet: bool = args.flux_controlnet
flux_controlnet_inpainting: bool = args.flux_controlnet_inpainting
flux_ipadapter: bool = args.flux_ipadapter
flux_turbo_alpha_lora: bool = args.flux_turbo_alpha_lora
hunyuan_enabled: bool = args.hunyuan_enabled
deepseek_enabled: bool = args.deepseek_enabled
sdxl_enabled: bool = args.sdxl_enabled
wan_enabled: bool = args.wan_enabled
wan_fun_enabled: bool = args.wan_fun_enabled

LOCAL_COMFY_BASE_DIR = "/usr/local/comfy"
LOCAL_COMFY_DIR = os.path.join(LOCAL_COMFY_BASE_DIR, "ComfyUI")
CUSTOM_NODES_DIR = os.path.join(LOCAL_COMFY_DIR, "custom_nodes")

os.system(f"mkdir -p {LOCAL_COMFY_BASE_DIR}")

os.chdir(LOCAL_COMFY_BASE_DIR)
os.system(f"git clone -b {comfy_tag} https://github.com/comfyanonymous/ComfyUI.git")

os.chdir(LOCAL_COMFY_DIR)
os.system("pip install xformers!=0.0.18 -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121")
os.system("pip install diffusers timm==1.0.9 addict yapf open-clip-torch python-dotenv clip-interrogator insightface onnxruntime rembg piexif aria2 ultralytics deepdiff evalidate surrealist simpleeval pynvml boto3 segment_anything redis fal_client gitpython triton replicate dghs-imgutils[gpu] sageattention decord bitsandbytes llama-cpp-python dill")

def clone_custom_node(owner_name: str, repo_name: str, co_name: str):
    os.chdir(CUSTOM_NODES_DIR)
    os.system(f"git clone --recursive https://github.com/{owner_name}/{repo_name}.git")
    os.chdir(os.path.join(CUSTOM_NODES_DIR, repo_name))
    os.system(f"git checkout {co_name}")
    os.chdir(CUSTOM_NODES_DIR)

os.chdir(CUSTOM_NODES_DIR)
os.system("git lfs install")
os.system(f"git clone --recursive -b {mgr_tag} https://github.com/ltdrdata/ComfyUI-Manager.git")
os.system("git clone --recursive -b 8.8.1 https://github.com/ltdrdata/ComfyUI-Impact-Pack.git")
os.system("git clone --recursive -b 1.2.9 https://github.com/ltdrdata/ComfyUI-Impact-Subpack.git")
os.system("git clone --recursive -b 1.13 https://github.com/ltdrdata/ComfyUI-Inspire-Pack.git")
os.system("git clone --recursive -b v1.2.7 https://github.com/yolain/ComfyUI-Easy-Use.git")

clone_custom_node("Suzie1", "ComfyUI_Comfyroll_CustomNodes", "d78b780")
clone_custom_node("Fannovel16", "comfyui_controlnet_aux", "1e9eac6377c882da8bb360c7544607036904362c")
clone_custom_node("Fannovel16", "ComfyUI-Frame-Interpolation", "c336f71")
clone_custom_node("Kosinkadink", "ComfyUI-Advanced-ControlNet", "b66cd70c9845a109a85b4a0ef13cefda41ca6039")
clone_custom_node("Kosinkadink", "ComfyUI-AnimateDiff-Evolved", "94eb45621c7e5a5286968b3938b1b7689d34ced0")
clone_custom_node("Kosinkadink", "ComfyUI-VideoHelperSuite", "4c7858ddd5126f7293dc3c9f6e0fc4c263cde079")
clone_custom_node("cubiq", "ComfyUI_IPAdapter_plus", "9d076a3df0d2763cef5510ec5ab807f6632c39f5")
clone_custom_node("cubiq", "ComfyUI_essentials", "33ff89f")
clone_custom_node("pythongosssss", "ComfyUI-Custom-Scripts", "bbda5e52ad580c13ceaa53136d9c2bed9137bd2e")
clone_custom_node("jags111", "efficiency-nodes-comfyui", "3ead4af")
clone_custom_node("BadCafeCode", "masquerade-nodes-comfyui", "432cb4d")
clone_custom_node("melMass", "comfy_mtb", "d87e52ea2c112fd95f257dcd6a54a5db77a34fc3")
clone_custom_node("FizzleDorf", "ComfyUI_FizzNodes", "7d6ea60")
clone_custom_node("alt-key-project", "comfyui-dream-project", "f48bed5b8ae866b3dad33fb811d712d45205f117")
clone_custom_node("kijai", "ComfyUI-KJNodes", "97d20e27e589854451a9d1f091f6524e947d6229")
clone_custom_node("kijai", "ComfyUI-Florence2", "90b012e922f8bb0482bcd2ae24cdc191ec12a11f")
clone_custom_node("kijai", "ComfyUI-Marigold", "1894ff2")
clone_custom_node("kijai", "ComfyUI-HunyuanVideoWrapper", "2b043839ae7abe58ae8d3ea6099daea2b7f53d17")
clone_custom_node("WASasquatch", "was-node-suite-comfyui", "3ed45af34a14551dc28cb3127235cc7197d4633f")
clone_custom_node("sipherxyz", "comfyui-art-venture", "50abaac")
clone_custom_node("rgthree", "rgthree-comfy", "32142fe476878a354dda6e2d4b5ea98960de3ced")
clone_custom_node("chrisgoringe", "cg-image-filter", "274896c27e7ca396546fa639ef5e9fbe3b2cbfbd")
clone_custom_node("crystian", "ComfyUI-Crystools", "72e2e9af4a6b9a58ca5d753cacff37ba1ff9bfa8")
clone_custom_node("TheBill2001", "comfyui-upscale-by-model", "f8bb900")
clone_custom_node("TinyTerra", "ComfyUI_tinyterraNodes", "b684adbcab271a2b7a3875bb97af27d495409a11")
clone_custom_node("ssitu", "ComfyUI_UltimateSDUpscale", "1b6e60d4f1e7ef325ea4b6268f41c03bd18eee5b")
clone_custom_node("evanspearman", "ComfyMath", "939bb81")
clone_custom_node("jamesWalker55", "comfyui-various", "5bd85aaf7616878471469c4ec7e11bbd0cef3bf2")
clone_custom_node("bash-j", "mikey_nodes", "a8c52735f51be160f115ee4b9ccd0ed758d3b520")
clone_custom_node("SuperBeastsAI", "ComfyUI-SuperBeasts", "f684c86")
clone_custom_node("storyicon", "comfyui_segment_anything", "ab63955")
clone_custom_node("aria1th", "ComfyUI-LogicUtils", "2451f43fa7322b2d82cf61e74c51bb202acaa85c")
clone_custom_node("XLabs-AI", "x-flux-comfyui", "0032855")
clone_custom_node("CY-CHENYUE", "ComfyUI-Janus-Pro", "cadecbd")
clone_custom_node("aigc-apps", "VideoX-Fun", "278a4c3cd29efd988f971fcecf62c4f31860beb6")
clone_custom_node("kijai", "ComfyUI-WanVideoWrapper", "949c887e0ca2c338455e7a4a9c28c147ef0aecb1")

os.chdir(os.path.join(CUSTOM_NODES_DIR, "VideoX-Fun"))
os.system("python install.py")
os.chdir(CUSTOM_NODES_DIR)

os.system(f"mkdir {os.path.join(LOCAL_COMFY_DIR, 'models', 'LLM')}")

os.chdir(os.path.join(CUSTOM_NODES_DIR, "ComfyUI-Janus-Pro"))
os.system("pip install -r requirements.txt")

def download(target:str, local_dir:str, threads:int, repo:str="DonatoDiffusion/trytonado"):
    url = f"https://huggingface.co/{repo}/resolve/main/{target}"
    file = os.path.basename(url)
    os.system(f"aria2c -c {url} -o {file} --console-log-level=error --file-allocation=none -x {threads} -s {threads} -k 50M -d {local_dir}")

os.chdir(os.path.join(LOCAL_COMFY_DIR, "models"))
os.system("git lfs install")

os.system('huggingface-cli download DonatoDiffusion/trytonado --include "ultralytics/*" --local-dir ./')
os.system('huggingface-cli download DonatoDiffusion/trytonado --include "upscale_models/*" --local-dir ./')
os.system('huggingface-cli download DonatoDiffusion/trytonado --include "insightface/*" --local-dir ./')

download("grounding-dino/groundingdino_swinb_cogcoor.pth", "./grounding-dino/", 16)
download("grounding-dino/groundingdino_swint_ogc.pth", "./grounding-dino/", 16)
download("grounding-dino/GroundingDINO_SwinB.cfg.py", "./grounding-dino/", 1)
download("grounding-dino/GroundingDINO_SwinT_OGC.cfg.py", "./grounding-dino/", 1)
download("sams/sam_hq_vit_h.pth", "./sams/", 16)
download("sd15/animatediff_models/v3_sd15_mm.ckpt", "./animatediff_models/", 16)
download("sd15/animatediff_models/motionModel_v03anime.ckpt", "./animatediff_models/", 16)
download("sd15/animatediff_motion_lora/v3_sd15_adapter.ckpt", "./animatediff_motion_lora/", 16)
download("sd15/controlnet/control_v11e_sd15_ip2p.pth", "./controlnet/", 16)
download("sd15/controlnet/control_v11f1e_sd15_tile.pth", "./controlnet/", 16)
download("sd15/controlnet/control_v11f1p_sd15_depth.pth", "./controlnet/", 16)
download("sd15/controlnet/control_v11p_sd15_lineart.pth", "./controlnet/", 16)
download("sd15/controlnet/control_v11p_sd15_openpose.pth", "./controlnet/", 16)
download("sd15/controlnet/control_v11e_sd15_ip2p.yaml", "./controlnet/", 1)
download("sd15/controlnet/control_v11f1e_sd15_tile.yaml", "./controlnet/", 1)
download("sd15/controlnet/control_v11f1p_sd15_depth.yaml", "./controlnet/", 1)
download("sd15/controlnet/control_v11p_sd15_lineart.yaml", "./controlnet/", 1)
download("sd15/controlnet/control_v11p_sd15_openpose.yaml", "./controlnet/", 1)
download("sd15/ipadapter/ip-adapter-plus_sd15.bin", "./ipadapter/", 16)
download("sd15/ipadapter/ip-adapter-faceid-plusv2_sd15.bin", "./ipadapter/", 16)
download("sd15/clip_vision/clip_vision_sd15.safetensors", "./clip_vision/", 16)
download("sd15/vae/kl-f8-anime2.safetensors", "./vae/", 16)
download("sd15/vae/orangemix.vae.pt", "./vae/", 16)
download("sd15/vae/sdVAEForAnime_v10.pt", "./vae/", 16)
download("sd15/vae/vae-ft-mse-840000-ema-pruned.ckpt", "./vae/", 16)

download("v1-5-pruned.safetensors", "./checkpoints/", 16, "stable-diffusion-v1-5/stable-diffusion-v1-5")

if sdxl_enabled:
    download("sdxl/checkpoints/illustriousXL_v01.safetensors", "./checkpoints/", 16)
    download("sdxl/animatediff_models/mm_sdxl_v10_beta.ckpt", "./animatediff_models/", 16)
    download("sdxl/clip_vision/clip_vision_sdxl.safetensors", "./clip_vision/", 16)
    download("sdxl/controlnet/controlnet-union-sdxl-1.0-promax.safetensors", "./controlnet/", 16)
    download("sdxl/ipadapter/ip-adapter-faceid-plusv2_sdxl.bin", "./ipadapter/", 16)
    download("sdxl/ipadapter/ip-adapter_xl.pth", "./ipadapter/", 16)
    download("sdxl/vae/sdxl_vae.safetensors", "./vae/", 16)

if flux_enabled or flux_fp8_enabled:
    if flux_enabled:
        download("flux1-dev/flux1-dev.safetensors", "./unet/", 16)
    if flux_fp8_enabled:
        download("flux1-dev/flux1-dev-fp8.safetensors", "./checkpoints/", 16)
    download("flux1-dev/ae.safetensors", "./vae/", 2)
    download("flux1-dev/clip_l.safetensors", "./clip/", 2)
    download("flux1-dev/t5xxl_fp16.safetensors", "./clip/", 16)
if flux_controlnet:
    download("flux1-dev/FLUX.1-dev-Controlnet-Union-Pro.safetensors", "./controlnet/", 16)
if flux_controlnet_inpainting:
    download("flux1-dev/FLUX.1-dev-Controlnet-Inpainting-Beta.safetensors", "./controlnet/", 16)
if flux_ipadapter:
    download("flux1-dev/flux-ip-adapter.safetensors", "./ipadapter/", 16)
if flux_turbo_alpha_lora:
    download("flux1-dev/flux1-turbo-alpha-lora.safetensors", "./loras/", 16)

if hunyuan_enabled:
    download("hunyuan_video_720_cfgdistill_fp8_e4m3fn.safetensors", "./diffusion_models/", 16, "Kijai/HunyuanVideo_comfy")
    download("hunyuan_video_vae_bf16.safetensors", "./vae/", 16, "Kijai/HunyuanVideo_comfy")
    download("split_files/text_encoders/clip_l.safetensors", "./text_encoders/", 16, "Comfy-Org/HunyuanVideo_repackaged")
    download("split_files/text_encoders/llava_llama3_fp8_scaled.safetensors", "./text_encoders/", 16, "Comfy-Org/HunyuanVideo_repackaged")

if deepseek_enabled:
    os.system("mkdir -p Janus-Pro")
    temp_cwd = os.getcwd()
    os.chdir(os.path.join(LOCAL_COMFY_DIR, "models", "Janus-Pro"))
    os.system('huggingface-cli download deepseek-ai/Janus-Pro-7B --include "*" --local-dir ./Janus-Pro-7B/')
    os.chdir(temp_cwd)

if wan_enabled or wan_fun_enabled:
    download("text_encoders/umt5-xxl-enc-bf16.safetensors", "./text_encoders/", 16)
    download("vae/Wan2_1_VAE_fp32.safetensors", "./vae/", 16)
    download("clip_vision/clip_vision_h.safetensors", "./clip_vision/", 16)
    if wan_enabled:
        download("split_files/diffusion_models/wan2.1_i2v_720p_14B_bf16.safetensors", "./diffusion_models/", 16, "Comfy-Org/Wan_2.1_ComfyUI_repackaged")
    if wan_fun_enabled:
        download("diffusion_models/Wan2.1-Fun-Control-14B_fp8_e4m3fn.safetensors", "./diffusion_models/", 16)


