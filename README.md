# AR-server

To handle the client request to localize a landmark from image.

## Getting Started

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/KOE-Wayfind/AR-server)

Choose 4-core CPU for faster processing (optional).

This Codespaces is configured with [NVIDIA CUDA](https://docs.github.com/en/codespaces/developing-in-codespaces/getting-started-with-github-codespaces-for-machine-learning#configuring-nvidia-cuda-for-your-codespace). It will automatically install cudnn and other dependencies.

> **Note**
> Free users have 120 core-hours per month and Pro users have 180 core-hours per month on GitHub Codespaces. The default codespace runs on a 2-core machine, so that's 60 hours (or 90 hours) of free usage per month before getting charged. Make sure to stop your codespace when you're not using it (it automatically stops after 30 minutes of inactivity by default). See more pricing details [here](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).

### Setup environment

Run

```bash
sudo apt update && sudo apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
```

Download & install custom [Hierarchical Localization](https://github.com/KOE-Wayfind/Hierarchical-Localization) package. (Slightly modified from version 1.3)

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

This process would take roughly ~10 minutes. At the end, you would get something like:
```console
[2023/07/04 02:47:32 hloc INFO] Reconstruction statistics:
Reconstruction:
        num_reg_images = 57
        num_cameras = 1
        num_points3D = 2656
        num_observations = 14258
        mean_track_length = 5.36822
        mean_observations_per_image = 250.14
        mean_reprojection_error = 0.971601
        num_input_images = 70
```

### Start the server

```bash
pip install -r requirements.txt
python app.py
```

The server will run on localhost:5000

### Test the API

Use the Thunder Client installed (the lightning icon). Import the sample `thunder-collection_Hloc API.json` to Thunder Client.

Try run the `Hloc API/Localize me` request.

The `image_data` in the example request is this image:

![conf-a](https://github.com/KOE-Wayfind/AR-server/assets/60868965/846b38be-542e-4565-b16f-9bdd33cfa18c)

So, the expected result is as follows:

```
{
  "result": "Conference Room A"
}
```

To test with your image, decode the image to Base64. You might want to resize to 512*512 px first. You can use [Image to Base64 encoder](https://base64.guru/converter/encode/image)

## Add to KOE-Wayfinder App

> **Note**
> We are running a development server. Ideally we would want to deploy the server to WSGI server environ (learn more [here](https://flask.palletsprojects.com/en/2.3.x/deploying/)). But since we are just testing, then I think it is okay. 🙈

To assign this server to [KOE-Wayfinder App](https://github.com/KOE-Wayfind/KOE-Wayfinder-App), follow the steps below.

### Make port public

Go to PORTS tab.

![Alt text](https://github.com/KOE-Wayfind/AR-server/assets/60868965/2cf3e9e2-24f9-4170-aef0-e8345c6fcb27)

Find the port **`5000`** from the list (named **Server Endpoint**). Change the port visibility from private to **public**.

### Obtain server URL

On the same port information, copy its address. Example: `https://iqfareez-improved-fishstick-q45gqxjgrjg24qqx-5000.preview.app.github.dev/`

### Assign to application

You have two options, either update from the source code or from the app settings.

From **source code**, navigate to `Assets/Scripts/LocalizationSettings.cs` and update `serverUrl` player prefs default value.
 
Or, in app in localization page, open the **localization setting** and update the URL directly.

## Limitations and known issues

- Sometimes, when you send image from client, the server will respond `400` error or other error. Try kill and restart the server (you may need to do it few times), the server will fix itself. You can also test with Insomnia or Postman to debug the request.
- The server can handle only one request at a time. _Well technically this Flask server can handle concurrent users_, but the `image` endpoint (localization process) can only run single process at one time.
