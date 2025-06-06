from dotenv import load_dotenv
import os
from legent.pipeline import AccidentPipeline
import sys

if __name__ == "__main__":
    load_dotenv()  # .env 파일에서 환경변수 불러오기
    api_key = os.environ.get("LEGENT_API_KEY")
    if not api_key:
        print("LEGENT_API_KEY not found in .env file.")
        sys.exit(1)
    if len(sys.argv) < 3:
        print("Usage: python run_legent.py <VIDEO_PATH> <PROMPT>")
        sys.exit(1)
    video_path = sys.argv[1]
    prompt = sys.argv[2]
    pipeline = AccidentPipeline(api_key=api_key)
    result = pipeline.run(video_path, prompt)
    print(result) 