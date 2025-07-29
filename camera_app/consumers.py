import json
import base64
import numpy as np
import cv2
import os
from channels.generic.websocket import WebsocketConsumer
from ultralytics import YOLO 


MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'dnn_models', 'yolov8n.pt')


CONF_THRESHOLD = 0.5


class CameraConsumer(WebsocketConsumer):

    model = YOLO(MODEL_PATH)

    def connect(self):
        self.accept()
        print("WebSocket bağlantısı kuruldu!")
        self.send(text_data=json.dumps({
            'message': 'WebSocket bağlantısı başarıyla kuruldu!'
        }))

    def disconnect(self, close_code):
        print("WebSocket bağlantısı kapandı:", close_code)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if 'frame' in text_data_json:
            frame_data = text_data_json['frame']
            format, imgstr = frame_data.split(';base64,')
            data = base64.b64decode(imgstr)

            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                print("Görüntü çözülemedi. Hatalı base64 verisi olabilir.")
                return


            results = self.model(frame, conf=CONF_THRESHOLD, classes=[0], verbose=False) 

            detected_boxes_for_frontend = []
            person_count = 0


            for r in results:

                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist() 
                    conf = box.conf[0].item()            
                    cls = int(box.cls[0].item())          


                    if cls == 0: 
                        x = int(x1)
                        y = int(y1)
                        w = int(x2 - x1)
                        h = int(y2 - y1)
                        detected_boxes_for_frontend.append([x, y, w, h])
                        person_count += 1
            

            self.send(text_data=json.dumps({
                'boxes': detected_boxes_for_frontend,
                'person_count': person_count
            }))

        elif 'message' in text_data_json:
            message = text_data_json['message']
            print(f"İstemciden gelen mesaj: {message}")
            self.send(text_data=json.dumps({
                'message': f'Sunucudan yanıt: {message}'
            }))