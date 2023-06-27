# AR-server

To handle the client request to localize a landmark from image.

## Getting Started

You'll need a Linux machine,

or just 

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/KOE-Wayfind/AR-server)

Choose 4-core CPU for faster processing (optional).

When Codespaces is started, it will automatically configured with [NVIDIA CUDA](https://docs.github.com/en/codespaces/developing-in-codespaces/getting-started-with-github-codespaces-for-machine-learning#configuring-nvidia-cuda-for-your-codespace) for faster processing.

### Setup environment

Run

```bash
sudo apt update && sudo apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
```

Download & install custom [Hierarchical Localization](https://github.com/KOE-Wayfind/Hierarchical-Localization) package

```bash
git clone --recursive https://github.com/KOE-Wayfind/Hierarchical-Localization
cd Hierarchical-Localization
pip install -e .
pip install --upgrade plotly
cd ..
```

Download [KOE Image Dataset](https://github.com/KOE-Wayfind/koe-datasets)

```bash
git clone https://github.com/KOE-Wayfind/koe-datasets.git
```

### Run the trainer script

```bash
python my_hloc.py
```

### Start the server

```bash
python app.py
```

### Test the API

Install Thunder Client in the VSCode (Default GitHub Codespaces will install this automaticaly). Import the sample `thunder-collection_Hloc API.json` to Thunder Client.

To test with your image, decode the image to Base64. You might want to resize to 512*512 px first. You can use [Image to Base64 encoder](https://base64.guru/converter/encode/image)


### Make port public (for GitHub Codespace)

This is an optional step. If you want the server to be accessed to the outside world.

Go to ports, right click on the port `5000`. Change private to public.
