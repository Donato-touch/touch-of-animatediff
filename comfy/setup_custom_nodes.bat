@echo off

GOTO:MAIN

:cloneCustomNode
    SETLOCAL ENABLEDELAYEDEXPANSION
        git clone --recursive https://github.com/%1/%2.git
        pushd %2
        git checkout %3
        popd
    ENDLOCAL
EXIT /b 0

:cloneCustomNodeByTag
    SETLOCAL ENABLEDELAYEDEXPANSION
        git clone --recursive -b %3 https://github.com/%1/%2.git
    ENDLOCAL
EXIT /b 0

:MAIN

md models\animatediff_models
md models\animatediff_motion_lora
md models\checkpoints
md models\clip
md models\clip_vision
md models\configs
md models\controlnet
md models\diffusers
md models\diffusion_models
md models\embeddings
md models\grounding-dino
md models\insightface\models
md models\ipadapter
md models\LLM
md models\loras
md models\onnx
md models\reactor
md models\rembg
md models\sams
md models\style_models
md models\ultralytics
md models\unet
md models\upscale_models
md models\vae
md models\vae_approx

IF [%1]==[] (
    set COMFY_DIR=ComfyUI_windows_portable
) ELSE (
    set COMFY_DIR=%1
)

md input
md output
pip install pyyaml
python make_extra_model_paths.py
move extra_model_paths.yaml %COMFY_DIR%\ComfyUI\
move run_nvidia_gpu_my.bat %COMFY_DIR%\ComfyUI\

%COMFY_DIR%\python_embeded\python.exe -m pip install "numpy<2"
%COMFY_DIR%\python_embeded\python.exe -m pip install insightface-0.7.3-cp312-cp312-win_amd64.whl onnx==1.16.1 onnxruntime-gpu==1.19.2
%COMFY_DIR%\python_embeded\python.exe -m pip install -r requirements.txt

pushd %COMFY_DIR%\ComfyUI\custom_nodes
git clone --recursive -b 2.54 https://github.com/comfyanonymous/ComfyUI.git
call:cloneCustomNode "Suzie1" "ComfyUI_Comfyroll_CustomNodes" "d78b780"
call:cloneCustomNode "Fannovel16" "comfyui_controlnet_aux" "5a049bd"
call:cloneCustomNode "Fannovel16" "ComfyUI-Frame-Interpolation" "c336f71"
call:cloneCustomNode "Kosinkadink" "ComfyUI-Advanced-ControlNet" "172543b"
call:cloneCustomNode "Kosinkadink" "ComfyUI-AnimateDiff-Evolved" "b3e508a"
call:cloneCustomNode "Kosinkadink" "ComfyUI-VideoHelperSuite" "05f085e"
call:cloneCustomNode "cubiq" "ComfyUI_IPAdapter_plus" "b188a6c"
call:cloneCustomNode "cubiq" "ComfyUI_essentials" "5a4e5cd"
call:cloneCustomNodeByTag "ltdrdata" "ComfyUI-Impact-Pack" "7.14"
call:cloneCustomNodeByTag "ltdrdata" "ComfyUI-Inspire-Pack" "1.9"
call:cloneCustomNode "pythongosssss" "ComfyUI-Custom-Scripts" "d6657cc"
call:cloneCustomNode "jags111" "efficiency-nodes-comfyui" "3ead4af"
call:cloneCustomNode "BadCafeCode" "masquerade-nodes-comfyui" "432cb4d"
call:cloneCustomNode "melMass" "comfy_mtb" "ecbb220"
call:cloneCustomNode "FizzleDorf" "ComfyUI_FizzNodes" "7d6ea60"
call:cloneCustomNode "alt-key-project" "comfyui-dream-project" "b9e6959"
call:cloneCustomNode "kijai" "ComfyUI-KJNodes" "2838126"
call:cloneCustomNode "kijai" "ComfyUI-Florence2" "27714ba"
call:cloneCustomNode "kijai" "ComfyUI-Marigold" "1894ff2"
call:cloneCustomNode "WASasquatch" "was-node-suite-comfyui" "fe7e088"
call:cloneCustomNode "sipherxyz" "comfyui-art-venture" "50abaac"
call:cloneCustomNode "rgthree" "rgthree-comfy" "70756c0"
call:cloneCustomNode "chrisgoringe" "cg-image-picker" "aaab0d3"
call:cloneCustomNode "crystian" "ComfyUI-Crystools" "03a61d6"
call:cloneCustomNode "TheBill2001" "comfyui-upscale-by-model" "f8bb900"
call:cloneCustomNode "un-seen" "comfyui-tensorops" "d34488e"
call:cloneCustomNode "TinyTerra" "ComfyUI_tinyterraNodes" "0387940"
call:cloneCustomNode "ssitu" "ComfyUI_UltimateSDUpscale" "e617ff2"
call:cloneCustomNode "evanspearman" "ComfyMath" "939bb81"
call:cloneCustomNode "jamesWalker55" "comfyui-various" "36454f9"
call:cloneCustomNode "bash-j" "mikey_nodes" "637bc18"
call:cloneCustomNode "SuperBeastsAI" "ComfyUI-SuperBeasts" "f684c86"
call:cloneCustomNode "storyicon" "comfyui_segment_anything" "ab63955"
call:cloneCustomNode "aria1th" "ComfyUI-LogicUtils" "2e65bc8"
call:cloneCustomNode "XLabs-AI" "x-flux-comfyui" "0032855"

pushd ComfyUI-Impact-Pack
..\..\..\python_embeded\python.exe install.py
popd

popd

pause
