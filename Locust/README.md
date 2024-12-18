## Headless

locust -f locust/locust_api_scripts/sample_perf.py --host=https://sample.com --users 10 --spawn-rate 1 --run-time 10m --csv locust/locust_api_scripts/result/sample_perf --html locust/locust_api_scripts/result/sample_perf.html --headless
