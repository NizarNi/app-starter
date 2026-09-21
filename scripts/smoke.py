"""Verify the running local Compose stack through its published HTTP ports."""

import json
from html.parser import HTMLParser
from urllib.request import urlopen


class PageText(HTMLParser):
    """Read rendered text, excluding hydration scripts and HTML comments."""

    def __init__(self) -> None:
        super().__init__()
        self.heading: list[str] = []
        self.status: list[str] = []
        self.current: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h1":
            self.current = self.heading
        elif tag == "p" and dict(attrs).get("role") == "status":
            self.current = self.status

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h1", "p"}:
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.current.append(data)


def main() -> None:
    for path, expected in (("health", "ok"), ("ready", "ready")):
        with urlopen(f"http://127.0.0.1:8000/{path}", timeout=5) as response:
            assert response.status == 200, f"/{path} did not return HTTP 200"
            assert json.load(response) == {"status": expected, "service": "backend"}
        print(f"PASS backend /{path}")

    with urlopen("http://127.0.0.1:3000/", timeout=5) as response:
        assert response.status == 200, "Frontend did not return HTTP 200"
        page = PageText()
        page.feed(response.read().decode("utf-8"))
    assert "".join(page.heading).strip() == "App Starter", "Landing page is missing"
    assert "".join(page.status).strip() == "Backend status: connected (ok)", (
        "Frontend did not render a successful backend health response"
    )
    print("PASS frontend landing page and frontend → backend communication")


if __name__ == "__main__":
    main()
