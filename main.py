from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(
    title="HTTP Status Codes API",
    description="An API that returns different HTTP status codes",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the HTTP Status Codes API",
        "endpoints": {
            "success": "/success/{code}",
            "error": "/error/{code}",
            "redirect": "/redirect/{code}",
        },
    }


@app.get("/success/{code}")
async def success_codes(code: int):
    success_codes = [200, 201, 202, 203, 204, 205, 206]
    if code not in success_codes:
        raise HTTPException(status_code=400, detail="Invalid success status code")
    return JSONResponse(
        status_code=code,
        content={"status": code, "message": f"Success status code {code}"},
    )


@app.get("/error/{code}")
async def error_codes(code: int):
    error_codes = [
        400,
        401,
        403,
        404,
        405,
        406,
        407,
        408,
        409,
        410,
        411,
        412,
        413,
        414,
        415,
        416,
        417,
        418,
        421,
        422,
        423,
        424,
        425,
        426,
        428,
        429,
        431,
        451,
        500,
        501,
        502,
        503,
        504,
        505,
        506,
        507,
        508,
        510,
        511,
    ]
    if code not in error_codes:
        raise HTTPException(status_code=400, detail="Invalid error status code")
    return JSONResponse(
        status_code=code,
        content={"status": code, "message": f"Error status code {code}"},
    )


@app.get("/redirect/{code}")
async def redirect_codes(code: int):
    redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
    if code not in redirect_codes:
        raise HTTPException(status_code=400, detail="Invalid redirect status code")
    return JSONResponse(
        status_code=code,
        content={"status": code, "message": f"Redirect status code {code}"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
