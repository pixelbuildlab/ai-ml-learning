from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def home():
    return HTMLResponse("""
                     <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" id="file">
        <button type="submit">Upload</button>

    </form>
</body>

</html>
                        
                        """)


@app.post("/upload")
async def up(file: UploadFile = File(...)):
    total = 0
    with open("file", "wb") as ff:

        while chunk := await file.read(1024 * 1024 * 10):
            print("chunks", total)
            ff.write(chunk)
            total += 1
    return {"ok": True}
