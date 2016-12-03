
import v4l2capture
import Tkinter as tk
import select
import cv2
from time import sleep


class MainWindow(tk.Tk):
    camera_states = {True: "Camera is busy", False: "Camera is not busy"}
    in_out_states = {True: "video is saving", False: "video isn't saving"}
    def __init__(self):
        tk.Tk.__init__(self)
        self.camera = v4l2capture.Video_device('/dev/video0')
        self.camera.create_buffers(100)
        self.camera_busy = False
        self.frames = []
        self.in_out = False

        self.video_button = tk.Button(self, text="Video record", command=(lambda: self.capture_video(10)))
        self.video_button.pack(side=tk.TOP)

        self.photo_button = tk.Button(self, text="Photo")

        self.state_label = tk.Label(self)
        self.state_label.pack(side=tk.TOP)

        self.mainloop()


    def capture_video(self, lenght):
        self.camera.queue_all_buffers()
        self.camera_busy = True
        self.camera.start()
        for i in range(lenght * 10):
            select.select((self.camera,), (), ())
            image_data = self.camera.read_and_queue()
            self.frames.append(image_data)
        self.camera.stop()
        self.camera_busy = False
        print "Capture complited"
        fourcc = cv2.cv.CV_FOURCC('X', 'V', 'I', 'D')
        self.in_out = True
        out = cv2.VideoWriter('output.avi', fourcc, 10.0, (1280, 720))
        for image in self.frames:
            open('frame.jpg', 'wb').write(image)
            out.write(cv2.imread('frame.jpg'))
        out.release()
        self.frames = []
        print "Write complited"

    def update_state(self):
        while True:
            self.state_label.config(text="{0}, {1}.".format(self.camera_states[self.camera_busy],
                                                            self.in_out_states[self.in_out]))
            sleep(1)


if __name__ == "__main__":
    MainWindow()