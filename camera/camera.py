import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self, src, threshold, label_path, detector):
        self.id = src
        self.camera = cv2.VideoCapture(self.id)
        self.threshold = threshold
        self.labels = self.load_label(label_path)
        self.detector = detector
        self.image_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.image_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.inputs_width = self.detector.inputs_width
        self.inputs_height = self.detector.inputs_height
    
    def __del__(self):
        self.camera.release()
   
    def load_label(self, path, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as f:
            lines = f.readlines()
            if not lines:
                return {}
            if lines[0].split(' ', maxsplit=1)[0].isdigit():
                pairs = [line.split(' ', maxsplit=1) for line in lines]
                return {int(index): label.strip() for index, label in pairs}
            else:
                return {index: line.strip() for index, line in enumerate(lines)}

    def get_frame(self):
        # Acquire frame and resize to expected shape [1xHxWx3]
        ret, frame = self.camera.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(
            frame_rgb, (self.inputs_width, self.inputs_height))
        input_data = np.expand_dims(frame_resized, axis=0)

        (boxes, classes, scores) = self.detector.detect(input_data, self.id)

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if (scores[i] > self.threshold):
                ymin = int(max(1, (boxes[i][0] * self.image_height)))
                xmin = int(max(1, (boxes[i][1] * self.image_width)))
                ymax = int(
                    min(self.image_height, (boxes[i][2] * self.image_height)))
                xmax = int(
                    min(self.image_width, (boxes[i][3] * self.image_width)))

                cv2.rectangle(frame, (xmin, ymin),
                              (xmax, ymax), (10, 255, 0), 4)

                # Draw label
                object_name = self.labels[int(classes[i])]
                label = '%s: %d%%' % (object_name, int(scores[i]*100))
                print(label)
                labelSize, baseLine = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                label_ymin = max(ymin, labelSize[1] + 10)
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (
                    xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xmin, label_ymin-7),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        return cv2.imencode('.jpg', frame)[1].tobytes()
