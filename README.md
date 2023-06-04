# AR-server

## Getting Started

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/KOE-Wayfind/AR-server)

### Setup environment

Run

```bash
sudo apt update && sudo apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
```

[[Source]](https://stackoverflow.com/a/67088720/13617136) If failed, just try again. Then, run:

```bash
pip install ipywidgets widgetsnbextension pandas-profiling
```

<!-- And add the code block with contents

```bash
!jupyter nbextension enable --py widgetsnbextension
``` -->

Download & install custom [Hierarchical Localization](https://github.com/KOE-Wayfind/Hierarchical-Localization) package

```bash
git clone --recursive https://github.com/KOE-Wayfind/Hierarchical-Localization
cd Hierarchical-Localization
pip install -e .
pip install --upgrade --quiet plotly
```

Return back to the root directory

```bash
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
```

### Open port forwarding

```
```