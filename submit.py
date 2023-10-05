import requests

res = requests.post(url="https://eventretrieval.one/api/v1/login",
                    json={
                        "username": "gigachad",
                        "password": "AiL2Oaf8"
                    })
sessionId = res.json()["sessionId"]

_ = 1
while (True):
    print(f"Submission {_}:")
    _ = _ + 1
    videoId = input("Video Id: ")
    frameId = input("Frame Id: ")
    data = {
        "item": videoId,
        "frame": frameId,
        "session": sessionId,
    }
    res = requests.get(url="https://eventretrieval.one/api/v1/submit",
                       params=data)
    print("-"*100)
    print(f"Status code: {res.status_code}")
    print(f"Body: {res.json()}")
    print("\n\n" + "="*100)
