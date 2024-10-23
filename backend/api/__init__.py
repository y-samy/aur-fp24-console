from robot.navigation.boxes import BoxHandler
from robot.vision.camera import VideoCamera
from robot.vision.decoding import QR

box_handler = BoxHandler()
qr_decoder = QR(receiver_function=box_handler.receive_coords)
camera = VideoCamera(scanner_function=qr_decoder.decode, camera_number=1)