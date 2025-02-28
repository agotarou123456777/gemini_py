import cv2
import os
from datetime import datetime, timedelta
from pathlib import Path
import shutil

def extract_video_frames(file, export_fps):
    
    cap = cv2.VideoCapture(file)
    
    if not cap.isOpened():
        print(f"Error: cannot Open video => {file}")
        return None, None

    frames = []
    timestamps = []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("** Video Infomation **")
    print(f"total frame : {total_frames} frames")
    print(f"fps : {fps} frame/sec")
    
    frame_count = 0
    export_count = 1
    while True:
        print(f"read frame : {frame_count + 1} / {total_frames}\r", end = "")
        
        timestamp = frame_count / fps
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count == 0 or frame_count == total_frames -1:
            frames.append(frame)
            timestamps.append(timestamp)
            
        elif export_count * export_fps <= timestamp:
            frames.append(frame)
            timestamps.append(timestamp)
            export_count += 1
        
        frame_count += 1
        
    cap.release()
    
    return frames, timestamps

def add_seconds_to_now(base, add):
    added_time = base + timedelta(seconds = add)
    return added_time

# file setting
file_name = "KVID0169.mp4"
#file_name = "test.mp4"
resource_dir = "resources"
export_dir = "export"
export_fps = 0.2
webp_quality = 90
# text format setting
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 3
color = (0, 255, 0)
thickness = 4
position = (10, 80)

if __name__ == "__main__":
    target_file = os.path.join(resource_dir, file_name)
    frames, timestamps = extract_video_frames(target_file, export_fps)
    
    output_dir = Path(os.path.join(export_dir, file_name.split(".")[0]))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    base_time = datetime.now()
    if frames != None:
        for idx, frame in enumerate(frames):
            
            ts = timestamps[idx]
            datetime_ts = str(add_seconds_to_now(
                base = base_time, 
                add = timestamps[idx])).split(" ")[1][:-3]
            file_num = f"{idx:04d}"
            export_file = os.path.join(output_dir, f"frame_{file_num}.webp")
            print(export_file)
            
            cv2.putText(frame, datetime_ts, position, font, font_scale, color, thickness)
            cv2.imwrite(export_file, frame, [cv2.IMWRITE_WEBP_QUALITY, webp_quality])
    
    