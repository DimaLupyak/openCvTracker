import cv2
import sys

W = 600
H = 400

def track(tracker_type, video, bbox):    
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()

    # Read video
    video = cv2.VideoCapture(video)
    ok, frame = video.read()
    resized_frame = cv2.resize(frame, (W, H))
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(resized_frame, bbox)

    while True:        
        # Read a new frame
        ok, frame = video.read()        
        if not ok: continue
        resized_frame = cv2.resize(frame, (W, H))
        # Update tracker
        ok, bbox = tracker.update(resized_frame)
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(resized_frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(resized_frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2) 
        # Display result
        cv2.imshow(tracker_type, resized_frame) 
        # Exit if ESC pressed
        if cv2.waitKey(1) == 27 : break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    tracker_types = ['KCF', 'BOOSTING', 'MIL', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
    input_video ='rtsp://Oleksii:eLtGk4Cb@31.42.173.15:8072'
    tracker_type = tracker_types[0]
    bbox = (287, 23, 86, 320)
    video = cv2.VideoCapture(input_video)
    ok, frame = video.read()
    resized_frame = cv2.resize(frame, (W, H))
    bbox = cv2.selectROI(resized_frame, False) 
    for tracker_type in tracker_types:
        track('MEDIANFLOW', input_video, bbox)