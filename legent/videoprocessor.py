import base64
from dataclasses import dataclass
from typing import List

import cv2


@dataclass
class VideoProcessor:
    """Sample frames from a video for LVLM processing."""

    frames_per_second_to_sample: int = 1

    def sample_frames_from_video(self, video_path: str) -> List[str]:
        """Return list of base64 encoded JPEG frames."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video {video_path}")

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = 1
        if video_fps > 0:
            interval = int(video_fps / self.frames_per_second_to_sample)
            frame_interval = max(interval, 1)

        frames = []
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                _, buffer = cv2.imencode('.jpg', frame)
                frames.append(base64.b64encode(buffer).decode('utf-8'))
            frame_count += 1
        cap.release()

        return frames
