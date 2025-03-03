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
md models\text_encoders
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
md %COMFY_DIR%\ComfyUI\models\LLM
pip install pyyaml
python make_extra_model_paths.py
move extra_model_paths.yaml %COMFY_DIR%\ComfyUI\
move run_nvidia_gpu_my.bat %COMFY_DIR%\

@REM %COMFY_DIR%\python_embeded\python.exe -m pip install "numpy<2"
@REM %COMFY_DIR%\python_embeded\python.exe -m pip install -r requirements.txt
@REM %COMFY_DIR%\python_embeded\python.exe -m pip install insightface-0.7.3-cp312-cp312-win_amd64.whl onnx==1.16.1 onnxruntime-gpu==1.19.2
@REM %COMFY_DIR%\python_embeded\python.exe -m pip install dghs-imgutils[gpu]

%COMFY_DIR%\python_embeded\python.exe -m pip install --force-reinstall wheel
%COMFY_DIR%\python_embeded\python.exe -m pip install -r requirements.txt
@REM %COMFY_DIR%\python_embeded\python.exe -m pip install --no-deps --force-reinstall "dghs-imgutils[gpu]" "pydantic>=2.7.0" "anyio" "httpcore==1.*" "matplotlib" "scikit-image" "timm==1.0.9" "pooch" "pymatting" "urllib3==1.26.20" "sympy==1.13.1" "Cython==3.0.11" "numpy<2"

pushd %COMFY_DIR%\ComfyUI\custom_nodes
git clone --recursive -b 3.27.8 https://github.com/ltdrdata/ComfyUI-Manager.git
call:cloneCustomNode "Suzie1" "ComfyUI_Comfyroll_CustomNodes" "d78b780"
call:cloneCustomNode "Fannovel16" "comfyui_controlnet_aux" "1e9eac6377c882da8bb360c7544607036904362c"
call:cloneCustomNode "Fannovel16" "ComfyUI-Frame-Interpolation" "c336f71"
call:cloneCustomNode "Kosinkadink" "ComfyUI-Advanced-ControlNet" "b66cd70c9845a109a85b4a0ef13cefda41ca6039"
call:cloneCustomNode "Kosinkadink" "ComfyUI-AnimateDiff-Evolved" "94eb45621c7e5a5286968b3938b1b7689d34ced0"
call:cloneCustomNode "Kosinkadink" "ComfyUI-VideoHelperSuite" "4c7858ddd5126f7293dc3c9f6e0fc4c263cde079"
call:cloneCustomNode "cubiq" "ComfyUI_IPAdapter_plus" "9d076a3df0d2763cef5510ec5ab807f6632c39f5"
call:cloneCustomNode "cubiq" "ComfyUI_essentials" "33ff89f"
call:cloneCustomNodeByTag "ltdrdata" "ComfyUI-Impact-Pack" "8.8.1"
call:cloneCustomNodeByTag "ltdrdata" "ComfyUI-Impact-Subpack" "1.2.9"
call:cloneCustomNodeByTag "ltdrdata" "ComfyUI-Inspire-Pack" "1.13"
call:cloneCustomNode "pythongosssss" "ComfyUI-Custom-Scripts" "bbda5e52ad580c13ceaa53136d9c2bed9137bd2e"
call:cloneCustomNode "jags111" "efficiency-nodes-comfyui" "3ead4af"
call:cloneCustomNode "BadCafeCode" "masquerade-nodes-comfyui" "432cb4d"
call:cloneCustomNode "melMass" "comfy_mtb" "d87e52ea2c112fd95f257dcd6a54a5db77a34fc3"
call:cloneCustomNode "FizzleDorf" "ComfyUI_FizzNodes" "7d6ea60"
call:cloneCustomNode "alt-key-project" "comfyui-dream-project" "f48bed5b8ae866b3dad33fb811d712d45205f117"
call:cloneCustomNode "kijai" "ComfyUI-KJNodes" "97d20e27e589854451a9d1f091f6524e947d6229"
call:cloneCustomNode "kijai" "ComfyUI-Florence2" "90b012e922f8bb0482bcd2ae24cdc191ec12a11f"
call:cloneCustomNode "kijai" "ComfyUI-Marigold" "1894ff2"
call:cloneCustomNode "kijai" "ComfyUI-HunyuanVideoWrapper" "2b043839ae7abe58ae8d3ea6099daea2b7f53d17"
call:cloneCustomNode "WASasquatch" "was-node-suite-comfyui" "3ed45af34a14551dc28cb3127235cc7197d4633f"
call:cloneCustomNode "sipherxyz" "comfyui-art-venture" "50abaac"
call:cloneCustomNode "rgthree" "rgthree-comfy" "32142fe476878a354dda6e2d4b5ea98960de3ced"
call:cloneCustomNode "chrisgoringe" "cg-image-filter" "274896c27e7ca396546fa639ef5e9fbe3b2cbfbd"
call:cloneCustomNode "crystian" "ComfyUI-Crystools" "72e2e9af4a6b9a58ca5d753cacff37ba1ff9bfa8"
call:cloneCustomNode "TheBill2001" "comfyui-upscale-by-model" "f8bb900"
call:cloneCustomNode "TinyTerra" "ComfyUI_tinyterraNodes" "b684adbcab271a2b7a3875bb97af27d495409a11"
call:cloneCustomNode "ssitu" "ComfyUI_UltimateSDUpscale" "1b6e60d4f1e7ef325ea4b6268f41c03bd18eee5b"
call:cloneCustomNode "evanspearman" "ComfyMath" "939bb81"
call:cloneCustomNode "jamesWalker55" "comfyui-various" "5bd85aaf7616878471469c4ec7e11bbd0cef3bf2"
call:cloneCustomNode "bash-j" "mikey_nodes" "a8c52735f51be160f115ee4b9ccd0ed758d3b520"
call:cloneCustomNode "SuperBeastsAI" "ComfyUI-SuperBeasts" "f684c86"
call:cloneCustomNode "storyicon" "comfyui_segment_anything" "ab63955"
call:cloneCustomNode "aria1th" "ComfyUI-LogicUtils" "2451f43fa7322b2d82cf61e74c51bb202acaa85c"
call:cloneCustomNode "XLabs-AI" "x-flux-comfyui" "0032855"

popd

pause
