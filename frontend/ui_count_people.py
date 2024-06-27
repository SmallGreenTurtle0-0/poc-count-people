import streamlit as st
import requests
import cv2
import tempfile
import base64
import json


def get_result(image, type="path"):
    endpoint = "http://127.0.0.1:3000/people/count"
    headers = {"Content-Type": "application/json", "Accept": "text/plain"}
    payload = {"image": image, "type": type}
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    return response


def draw_boxes_on_image(image, box_dict_list):
    for box_dict in box_dict_list:
        confidence = box_dict["confidence"]
        box = box_dict["box"]
        x1, y1 = int(box["x1"]), int(box["y1"])
        x2, y2 = int(box["x2"]), int(box["y2"])

        cv2.rectangle(image, (x1, y1), (x2, y2), (175, 1, 134), 3)
        label = f"{confidence:.2f}"
        cv2.putText(
            image,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (175, 1, 134),
            2,
            cv2.LINE_AA,
        )

    return image


st.title("Count People App")
uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi", "mkv"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp4", dir="data"
    ) as tmp_file:
        tmp_file.write(uploaded_file.read())
        video_path = tmp_file.name
    st.video(video_path)

    def process_frame(frame, api_url="http://127.0.0.1:3000/people/count"):
        _, img_encoded = cv2.imencode(".jpg", frame)
        im_b64 = base64.b64encode(img_encoded).decode("utf8")
        response = get_result(im_b64, type="base64")
        if response.status_code == 200:
            json_result = response.json()
            count = json_result.get("people_count", 0)
            box_list = json_result.get("detail", None)
            box_list = json.loads(box_list)
        return box_list, count

    def process_video(input_path, output_path, frame_interval=10):
        cap = cv2.VideoCapture(input_path)
        frame_count = 0
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = None
        box_list = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                box_list, count = process_frame(frame)
            processed_frame = draw_boxes_on_image(frame.copy(), box_list)
            cv2.putText(
                processed_frame,
                f"People detected: {count}",
                (40, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 0, 0),
                2,
                cv2.LINE_AA,
            )

            if out is None:
                out = cv2.VideoWriter(
                    output_path, fourcc, 20.0, (frame.shape[1], frame.shape[0])
                )

            frame_count += 1
            out.write(processed_frame)

        cap.release()
        out.release()

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp4", dir="data"
    ) as output_tmp_file:
        processed_video_path = output_tmp_file.name

    process_video(video_path, processed_video_path, 20)
    st.video(processed_video_path)

    with open(processed_video_path, "rb") as f:
        st.download_button(
            "Download Processed Video", f, file_name="processed_video.mp4"
        )
