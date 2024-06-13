from aiohttp.web import run_app
from app import create_app


def main() -> None:
    app = create_app()
    run_app(app, port=8000)


if __name__ == "__main__":
    main()
