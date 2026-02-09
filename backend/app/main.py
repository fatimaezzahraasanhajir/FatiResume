import swagger_ui_bundle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Resume Match API",
        version="0.1.0",
        swagger_ui_parameters={
            "swagger_ui_css_url": "/static/swagger/swagger-ui.css",
            "swagger_ui_js_url": "/static/swagger/swagger-ui-bundle.js",
            "swagger_ui_standalone_preset_js_url": "/static/swagger/swagger-ui-standalone-preset.js",
        },
    )

    app.mount(
        "/static/swagger",
        StaticFiles(directory=swagger_ui_bundle.swagger_ui_path),
        name="swagger-ui",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
