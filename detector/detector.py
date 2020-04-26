from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate
import threading

class Detector(object):
    def __init__(self, model_path, edgetpu):
        self.interpreter = self.create_interpreter(model_path, edgetpu)
        self.model_input_details = self.interpreter.get_input_details()
        self.model_output_details = self.interpreter.get_output_details()
        self.inputs_height = self.interpreter.get_input_details()[0]['shape'][1]
        self.inputs_width = self.interpreter.get_input_details()[0]['shape'][2]
        self.lock = threading.Lock()

    def create_interpreter(self, model, edgetpu):
        if edgetpu:
            interpreter = Interpreter(model, experimental_delegates=[
                load_delegate('libedgetpu.so.1.0')])
        else:
            interpreter = Interpreter(model)
        interpreter.allocate_tensors()
        return interpreter

    def detect(self, input_tensors, camera_id):
        boxes = None
        classes = None
        scores = None
        self.lock.acquire()
        print("Inferencing on source:", camera_id)

        # set frame as input tensors
        self.interpreter.set_tensor(
            self.model_input_details[0]['index'], input_tensors)

        # perform inference
        self.interpreter.invoke()

        # Get output tensor
        boxes = self.interpreter.get_tensor(
            self.model_output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(
            self.model_output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(
            self.model_output_details[2]['index'])[0]

        self.lock.release()
        return (boxes, classes, scores)
