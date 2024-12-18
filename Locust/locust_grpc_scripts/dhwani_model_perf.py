from locust import events, task

from grpc_user import grpc_user
from grpc_proto import dhwani_model_pb2_grpc, dhwani_model_pb2
import random, os
import base64


# Get the current directory (relative to this script)
script_dir = os.path.dirname(os.path.abspath(__file__))


payloads = [
    {
        "file_path": os.path.join(script_dir, "/resampled_audio/bengala.mp3"),
        "src_lang_code": "ben",
        "tgt_lang_code": "eng"
    },
    {
        "file_path": os.path.join(script_dir, "/resampled_audio/English_new.mp3"),
        "src_lang_code": "eng",
        "tgt_lang_code": "hin"
    },
    {
        "file_path": os.path.join(script_dir, "/resampled_audio/hin.mp3"),
        "src_lang_code": "hin",
        "tgt_lang_code": "eng"
    },
    {
        "file_path": os.path.join(script_dir, "/resampled_audio/Malyalam_new.wav"),
        "src_lang_code": "mal",
        "tgt_lang_code": "eng"
    },
    {
        "file_path": os.path.join(script_dir, "/resampled_audio/Marathi_new.mp3"),
        "src_lang_code": "mar",
        "tgt_lang_code": "eng"
    },
    {
        "file_path": os.path.join(script_dir, "/resampled_audio/Tamil_new.mp3"),
        "src_lang_code": "tam",
        "tgt_lang_code": "eng"
    },
    {
        "file_path": os.path.join(script_dir, "/resampled_audio/Telugu.mp3"),
        "src_lang_code": "tel",
        "tgt_lang_code": "eng"
    }
]

ISO_TARGET_LANGUAGE_MAP = {
          'eng': 'English',
          'hin': 'Hindi',
          'tel': 'Telugu',
        }
TASK_TYPE = {
    'Hindi': 's2tt_hi',
    'English': 's2tt_en',
    'Telugu': 's2tt_te'
    }


class WavProcessorUser(grpc_user.GrpcUser):
    # wait_time = constant(1)
    host = ""
    stub_class = dhwani_model_pb2_grpc.WavProcessorStub

    @task
    def grpc_client_task(self):
        payload = random.choice(payloads)
        tgt_lang_code = payload["tgt_lang_code"]
        task_type = TASK_TYPE[ISO_TARGET_LANGUAGE_MAP[tgt_lang_code]]
        
        file_path = payload["file_path"]
        with open(file_path, "rb") as wav_file:
            wav_data = wav_file.read()
            wav_data_base64 = base64.b64encode(wav_data).decode('utf-8')
        

        self.stub.ProcessWav(dhwani_model_pb2.WavRequest(
            wav_data_base64=wav_data_base64,
            task_type=task_type
        ))
