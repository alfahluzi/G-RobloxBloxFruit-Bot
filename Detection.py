# Using YOLOv5 object detection
from PIL import Image
import cv2 as cv
import torch
from threading import Thread, Lock

class Detection:
    STOPPED = True
    MODEL = None
    LOCK = None

    rectangles = []
    image = None
    image_result = None 
    debug = False
    active = False

    def __init__(self, model_path = 'model-v1.pt', conf = 0.35, classes = [], debug = False, customModel = True):
        '''
        [model_path] path to YOLOv5 model \n
        [conf] confidence of detecting, range 0 to 1 \n
        [classes] class label of your model \n
        [debug] print some result if True \n
        [customModel] using yolov5s.pt pretrained model if False \n
        '''
        print('Initiating Detection...')
        # ========================================================================
        self.LOCK = Lock()
        self.debug = debug
        if customModel:
            self.MODEL = torch.hub.load('yolov5', 'custom', source='local', path= model_path, force_reload=True)
        else:
            self.MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.MODEL.conf = conf
        if classes != []:
            self.MODEL.classes = classes # see on labels.txt at yolo-dataset
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", device)
        # ========================================================================
        print('Finish initiating Detection')
        
    def start(self):
        print('Staring detection...')
        self.STOPPED = False
        t = Thread(target=self._run)
        t.start()
        
    def stop(self):
        print('Stopping detection')
        self.STOPPED = True
    
    def getResult(self):
        return (self.image_result, self.rectangles)

    def update(self, screen):
        self.LOCK.acquire()
        self.image = screen
        self.LOCK.release()
    
    def setActive(self, isActive):
        self.LOCK.acquire()
        self.active = isActive
        self.LOCK.release()

    def _run(self):
        '''Dont use this function'''
        while not self.STOPPED:
            if not self.image is None:
                rect = []
                # Get Image
                arrimg = self.image
                if self.active:
                    # Processing Image
                    result = self.MODEL(Image.fromarray(arrimg))
                    # Draw Rectangle
                    resultDetail = result.pandas().xyxy[0]
                    color = (0,250,0)
                    for i in range(len(resultDetail.name)):
                        conf = resultDetail.confidence[i]
                        xyMin = (int(resultDetail.xmin[i]), int(resultDetail.ymin[i]))
                        xyMax = (int(resultDetail.xmax[i]), int(resultDetail.ymax[i]))
                        cv.putText(arrimg, f"{resultDetail.name[i]} ({conf:.2f})", xyMin, cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        cv.rectangle(arrimg, xyMin, xyMax, color, 2)
                        rect.append([xyMin[0], xyMin[1]])
                    rect.sort(reverse=False)
                    if len(rect) > 0:
                        if self.debug:
                            print('\n\n Result ============================================ \n', resultDetail)
                            print('\n\n Rectangles ======================================== \n', rect)
                else : cv.waitKey(10)
                self.LOCK.acquire()
                self.rectangles = rect
                self.image_result = arrimg
                self.LOCK.release()
        else : 
            if self.debug: print('No image to detect!')