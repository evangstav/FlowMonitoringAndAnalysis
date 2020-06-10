import cv2


class VideoCamera:
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('suits_hd.mp4')
        self.video = cv2.VideoCapture("/home/evangelos/Videos/Cat.mp4")
        # this can also be a stream

    def __del__(self):
        self.video.release()

    def get_frame_bytes(self):
        ret, frame = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tostring()

    def get_frame(self):
        ret, frame = self.video.read()
        return frame
