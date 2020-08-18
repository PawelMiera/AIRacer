from settings.settings import Values
import importlib.util
import cv2
import numpy as np


class Detector:
    def __init__(self, model_path, labels_path):
        with open(labels_path, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        if self.labels[0] == '???':
            del (self.labels[0])

        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter
            if Values.USE_EDGE_TPU:
                from tflite_runtime.interpreter import load_delegate
        else:
            from tensorflow.lite.python.interpreter import Interpreter
            if Values.USE_EDGE_TPU:
                from tensorflow.lite.python.interpreter import load_delegate
        if Values.USE_EDGE_TPU:
            self.interpreter = Interpreter(model_path=model_path,
                                           experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        else:
            self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        self.img_ind = 0
        print("Model init success!")

    def detect(self, frame):
        points = []
        image = cv2.resize(frame, (self.width, self.height))
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(image_rgb, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

        for i in range(len(scores)):
            if (scores[i] > Values.DETECTION_THRESHOLD) and (scores[i] <= 1.0):
                ymin = int(max(1, (boxes[i][0] * Values.CAMERA_HEIGHT)))
                xmin = int(max(1, (boxes[i][1] * Values.CAMERA_WIDTH)))
                ymax = int(min(Values.CAMERA_HEIGHT, (boxes[i][2] * Values.CAMERA_HEIGHT)))
                xmax = int(min(Values.CAMERA_WIDTH, (boxes[i][3] * Values.CAMERA_WIDTH)))

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                object_name = self.labels[int(classes[i])]
                label = '%s: %d%%' % (object_name, int(scores[i] * 100))
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                label_ymin = max(ymin, labelSize[1] + 10)

                cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                              (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                points.append(boxes[i])

                if Values.SHOW_IMAGES:
                    cv2.imshow("View", frame)
                    cv2.waitKey(1)

        return points
