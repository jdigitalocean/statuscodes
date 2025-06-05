from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn
import random
import asyncio
import os

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
            "server-error": "/server-error/{type}",
        },
    }


@app.get("/success/{code}")
async def success_codes(code: int):
    success_codes = [200, 201, 202, 203, 204, 205, 206]
    if code not in success_codes:
        raise HTTPException(status_code=400, detail="Invalid success status code")

    if code == 204:
        return Response(status_code=204, headers={"Cache-Control": "no-store"})

    return JSONResponse(
        status_code=code,
        content={"status": code, "message": f"Success status code {code}"},
        headers={"Cache-Control": "no-store"},
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

    response = JSONResponse(
        status_code=code,
        content={"status": code, "message": f"Error status code {code}"},
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
    return response


@app.get("/redirect/{code}")
async def redirect_codes(code: int):
    redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
    if code not in redirect_codes:
        raise HTTPException(status_code=400, detail="Invalid redirect status code")

    if code == 304:
        return Response(status_code=304, headers={"Cache-Control": "no-store"})

    return RedirectResponse(
        url="/", status_code=code, headers={"Cache-Control": "no-store"}
    )


def cause_division_error():
    return random.choice([1, 2, 3]) / 0


def cause_memory_error():
    return [1] * (10**9)


def cause_recursion_error():
    return cause_recursion_error()


def cause_type_error():
    return "string" + 123


def cause_key_error():
    return {}["nonexistent"]


def cause_index_error():
    return [][0]


def cause_attribute_error():
    return None.nonexistent


def cause_import_error():
    return __import__("nonexistent_module")


def cause_value_error():
    return int("not a number")


@app.get("/server-error/{type}")
async def server_error(type: str):
    error_handlers = {
        "random": cause_division_error,
        "memory": cause_memory_error,
        "recursion": cause_recursion_error,
        "type": cause_type_error,
        "key": cause_key_error,
        "index": cause_index_error,
        "attribute": cause_attribute_error,
        "import": cause_import_error,
        "value": cause_value_error,
    }

    if type not in error_handlers:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid error type. Available types: {', '.join(error_handlers.keys())}",
        )

    try:
        handler = error_handlers[type]
        if asyncio.iscoroutinefunction(handler):
            await handler()
        else:
            handler()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "error_type": type,
                "message": f"Server error: {str(e)}",
            },
            headers={
                "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )


def main():
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
