from dataclasses import dataclass
from typing import Optional

from .videoprocessor import VideoProcessor
from .lvlm_extractor import LVLMExtractor
from .info_parser import InformationParser
from .classifier import AccidentClassifier


@dataclass
class AccidentPipeline:
    """End-to-end pipeline to classify accidents from video."""

    api_key: str

    def run(self, video_path: str, prompt: str) -> Optional[str]:
        processor = VideoProcessor()
        frames = processor.sample_frames_from_video(video_path)

        extractor = LVLMExtractor(api_key=self.api_key)
        text_resp = extractor.query(frames, prompt)
        if text_resp is None:
            return None

        parser = InformationParser()
        info = parser.parse(text_resp)

        classifier = AccidentClassifier()
        return classifier.classify(info)
