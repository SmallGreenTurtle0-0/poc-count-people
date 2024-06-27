## Installation
`conda` virtual environment is recommended.
```bash
conda create -n poc_count_people python=3.9 -y
conda activate poc_count_people
git clone https://github.com/THU-MIG/yolov10 src_api/services/yolo/yolov10
chmod +x scripts/setup.sh
scripts/setup.sh
pre-commit install
```

## Usage
Copy the `.env.example` file, rename it to `.env`, and set the values for the variables.
Explanation of the .env.example file contents.
```bash

```

Run the following command to start the server.
```bash
chmod +x scripts/run_server.sh
scripts/run_server.sh
```

Run the following command to start the streamlit app.
```bash
chmod +x scripts/run_frontend.sh
scripts/run_frontend.sh
```

Sample request:
```bash
curl --location --request POST 'http://127.0.0.1:3000/people/count' \
--header 'Content-Type: application/json' \
--data '{
    "image": "data/dogcat.jpeg"
}'
```

## References
- [YOLOv10](https://github.com/THU-MIG/yolov10)
