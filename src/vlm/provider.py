from typing import Protocol


class VisionProvider(Protocol):

    def analyze_screenshot(
        self,
        image_path: str,
    ) -> dict: ...


class MockVisionProvider:

    def analyze_screenshot(
        self,
        image_path: str,
    ) -> dict:

        return {
            "source": image_path,
            "error_title": "Detected application error",
            "description": ("Screenshot analysis identified " "an application error."),
            "confidence": 0.0,
            "provider": "mock",
        }
