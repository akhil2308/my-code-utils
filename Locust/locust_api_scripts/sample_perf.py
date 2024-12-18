from locust import HttpUser, task, between, TaskSet, constant
import random

# Define a list of payloads to choose from randomly
payloads = [
    {
        "inputs":[ "Whether for the host computer or the GPU device, all CUDA source code is now processed according to C++ syntax rules.[24] This was not always the case. Earlier versions of CUDA were based on C syntax rules.[25] As with the more general case of compiling C code with a C++ compiler, it is therefore possible that old C-style CUDA source code will either fail to compile or will not behave as originally intended."],
        "target_language_code": "en-IN",
        "speaker": "meera"
    },
    {
        "inputs":[ "Interoperability with rendering languages such as OpenGL is one-way, with OpenGL having access to registered CUDA memory but CUDA not having access to OpenGL memory."],
        "target_language_code": "en-IN",
        "speaker": "meera"
    },
    {
        "inputs":[ "Copying between host and device memory may incur a performance hit due to system bus bandwidth and latency (this can be partly alleviated with asynchronous memory transfers, handled by the GPU's DMA engine)."],
        "target_language_code": "en-IN",
        "speaker": "meera"
    },
    {
        "inputs":[ "Threads should be running in groups of at least 32 for best performance, with total number of threads numbering in the thousands. Branches in the program code do not affect performance significantly, provided that each of 32 threads takes the same execution path; the SIMD execution model becomes a significant limitation for any inherently divergent task (e.g. traversing a space partitioning data structure during ray tracing)."],
        "target_language_code": "en-IN",
        "speaker": "meera"
    },
    {
        "inputs":[ "No emulation or fallback functionality is available for modern revisions."],
        "target_language_code": "en-IN",
        "speaker": "meera"
    },
    {
        "inputs":[ "In single-precision on first generation CUDA compute capability 1.x devices, denormal numbers are unsupported and are instead flushed to zero, and the precision of both the division and square root operations are slightly lower than IEEE 754-compliant single precision math. Devices that support compute capability 2.0 and above support denormal numbers, and the division and square root operations are IEEE 754 compliant by default."],
        "target_language_code": "en-IN",
        "speaker": "meera"
    }
]
class TTSRequestTaskSet(TaskSet):
    def on_start(self):
        self.api_subscription_key = "xxxxxxx"

    @task
    def send_tts_request(self):
        headers = {
            'api-subscription-key': self.api_subscription_key,
            'Content-Type': 'application/json'
        }

        # Randomly select a payload
        payload = random.choice(payloads)

        try:
            response = self.client.post(
                "/text-to-speech", 
                json=payload, 
                headers=headers,
            )
            response.raise_for_status()
        except Exception as e:
            print(f"There is an error: {e}")

class TTSUser(HttpUser):
    wait_time = constant(1)
    tasks = [TTSRequestTaskSet]
    host = "https://api.sarvam.ai"


# locust -f Locust_scripts/sarvam_ai/tts_perf.py --host=https://api.sarvam.ai --users 5 --spawn-rate 1 --run-time 2m --csv result/test_sarvam_ai_tts --html result/locust_test_sarvam_ai_tts.html --headless

# locust -f Locust_scripts/sarvam_ai/tts_perf.py --host=https://api.sarvam.ai --users 1 --spawn-rate 1 --run-time 5m --csv result/test_sarvam_ai_tts --html result/locust_test_sarvam_ai_tts.html --headless