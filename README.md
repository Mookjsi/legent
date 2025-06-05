# LEGENT - Legal Agent

This repository contains a simplified pipeline for classifying traffic accidents
based on video input. Frames are sampled from a video, analyzed by an external
vision language model (LVLM) such as OpenAI's GPT-4V, parsed into structured
data and then classified against predefined PDF rules.

## Structure

- `legent/videoprocessor.py` – samples frames from a video.
- `legent/lvlm_extractor.py` – queries the LVLM with frames and a prompt.
- `legent/info_parser.py` – converts LVLM textual output into a structured dict.
- `legent/classifier.py` – rule-based accident classifier (placeholder).
- `legent/pipeline.py` – orchestrates the end-to-end pipeline.

## Installation

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

```
from legent.pipeline import AccidentPipeline

API_KEY = "sk-..."  # OpenAI key
PROMPT = "..."       # Prompt following PDF guidelines
VIDEO = "accident.mp4"

pipeline = AccidentPipeline(api_key=API_KEY)
result = pipeline.run(VIDEO, PROMPT)
print(result)
```

The classifier currently implements only a basic rule for demonstration. Extend
`legent/classifier.py` with additional rules or integrate an ML model.
