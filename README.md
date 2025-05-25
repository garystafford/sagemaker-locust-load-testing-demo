# Finding Your LLM's Breaking Point

## Load Testing SageMaker Real-time Inference Endpoints with Locust

Learn how model size, instance choice, deployment configuration, and inference parameters impact requests-per-second and latency using Locust.

### Installation and Use

Create a virtual Python environment on Mac/Linux

```sh
python --version # I am using Python 3.13.2

python -m pip install virtualenv -Uqqq
python -m venv .venv
source .venv/bin/activate
```

Install Python package dependencies

```sh
python -m pip install pip -Uqqq
python -m pip install -r requirements.txt -Uqqq
```

Locust Commands

Make sure you update the `host` parameter in the Locust confif files, and update the `region`, and `endpoint_name` parameters in Python scripts.

```sh
# locust --config <filename>
locust --config locust_025_users.conf
locust --config locust_100_users.conf


```

Deactivate and delete virtual environment once you are done

```sh
deactivate
rm -rf .venv
```


