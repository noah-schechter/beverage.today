import requests
import time



def fetch():
    response = requests.get("https://imaginary-anteater-nest-dev.wayscript.cloud b")
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    start = time.perf_counter()
    fetch()
    end = time.perf_counter()
    print (end-start)