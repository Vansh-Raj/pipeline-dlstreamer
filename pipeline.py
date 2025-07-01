import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# Initialize GStreamer
Gst.init(None)

def on_message(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-of-stream")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, Debug: {debug}")
        loop.quit()

def main():
    # Build pipeline string
    pipeline_str = '''
    filesrc location=input.mp4 !
    decodebin !
    videoconvert !
    gvadetect model=ssd.xml device=GPU batch-size=1 !
    gvaclassify model=resnet.xml device=GPU batch-size=1 !
    gvawatermark !
    videoconvert !
    autovideosink
    '''

    # Create pipeline
    pipeline = Gst.parse_launch(pipeline_str)

    # Create GLib Main Loop
    loop = GObject.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message, loop)

    # Start pipeline
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    main()
