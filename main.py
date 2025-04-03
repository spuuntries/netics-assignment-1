from datetime import timedelta, datetime
from fastapi import FastAPI
import humanize
import uvicorn
import time


app = FastAPI()
START_TIME = time.time()


@app.get("/health")
async def health_check():
    uptime_seconds = int(time.time() - START_TIME)
    uptime_formatted = humanize.precisedelta(
        timedelta(seconds=uptime_seconds), format="%d"
    )

    return {
        "nama": "Faiz Muhammad Kautsar",
        "nrp": "5054231013",
        "status": "UP",
        "timestamp": datetime.now().isoformat(),
        "uptime": uptime_formatted,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
