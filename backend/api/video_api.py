from flask import Blueprint, Response
from api import qr_decoder, camera

video_api = Blueprint('video_api', __name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


@video_api.route("/feed")
def video_feed():
    return Response(
        gen(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

@video_api.route("/get_cameras")
def video_get_cameras():
    cameras = camera.get_sources()

@video_api.route("/set_camera/<i>")
def video_set_camera(i):
    camera.set_source(int(i))
    return Response(status=204)

@video_api.route("/feed/pause/<on_or_off>")
def video_pause_resume(on_or_off):
    if on_or_off == "on":
        if not camera.get_pause_state():
            camera.toggle_pause()
    elif on_or_off == "off":
        if camera.get_pause_state():
            camera.toggle_pause()

@video_api.route("/configure_scanning/<options>")
def video_configure_scanning(options):
    if options == "off":
        if camera.is_scanning():
            camera.toggle_scanning()
    else:
        if not camera.is_scanning():
            camera.toggle_scanning()
        qr_decoder.set_decoder(algorithm=options)
