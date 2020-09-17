from settings.settings import Values, Constants
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
        image = cv2.resize(frame, (self.width, self.height))
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(image_rgb, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

        height, width, channels = frame.shape
        good_scores = []
        good_boxes = []
        good_classes = []
        for i in range(len(scores)):
            if (scores[i] > Values.DETECTION_THRESHOLD) and (scores[i] <= 1.0):
                ymin = int(max(1, (boxes[i][0] * height)))
                xmin = int(max(1, (boxes[i][1] * width)))
                ymax = int(min(height, (boxes[i][2] * height)))
                xmax = int(min(width, (boxes[i][3] * width)))
                good_boxes.append(boxes[i])
                good_scores.append(scores[i])
                good_classes.append(classes[i])
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                object_name = self.labels[int(classes[i])]
                label = '%s: %d%%' % (object_name, int(scores[i] * 100))
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                label_ymin = max(ymin, labelSize[1] + 10)

                cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                              (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                if Values.SHOW_IMAGES:
                    cv2.imshow("View", frame)
                    cv2.waitKey(1)

        mids = self.check_detections(good_boxes, good_classes, good_scores)
        rad = 4
        for mid in mids:
            frame = cv2.circle(frame, (int(mid[0]*width), int(mid[1]*height)), rad, (0, 0, 255), 2)
            rad += 6


        return 0

    def check_detections(self, boxes, classes, scores):
        corners_ind = []
        gate_ind = []
        corners = 0
        corners_score = 0
        gate_score = 0
        mids = []
        for i in range(len(scores)):
            if int(classes[i]) == Constants.LD or int(classes[i]) == Constants.LU \
                    or int(classes[i]) == Constants.RD or int(classes[i]) == Constants.RU:
                corners_score += scores[i]
                corners += 1
                corners_ind.append(i)
            else:
                gate_score = scores[i]
                gate_ind.append(i)
        corners_score /= corners
        #print("c", corners_score, "g", gate_score)

        corner_mids = []
        for ind in corners_ind:
            max_y = boxes[ind][2]
            min_y = boxes[ind][0]
            max_x = boxes[ind][3]
            min_x = boxes[ind][1]
            c_mid = (min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2)
            corner_mids.append(c_mid)

        corner_mid = np.mean(corner_mids, axis=0)
        mids.append(corner_mid)

        for ind in gate_ind:
            max_y = boxes[ind][2]
            min_y = boxes[ind][0]
            max_x = boxes[ind][3]
            min_x = boxes[ind][1]
            gate_mid = [min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2]
            mids.append(gate_mid)


        return mids

        """print(scores[i], end=" ")
        print("classes ", end="")
        print(classes[i], end=" ")"""

        """print(" " + str(corners))
        print()"""