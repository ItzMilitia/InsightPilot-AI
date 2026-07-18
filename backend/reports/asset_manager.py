"""
Enterprise Asset Manager.

Responsible for managing static assets used by report engines,
including CSS, JavaScript, images, fonts, and other resources.
"""

from __future__ import annotations

from pathlib import Path


class AssetManager:
    """
    Enterprise Asset Manager.

    Responsibilities
    ----------------
    - Resolve asset paths
    - Validate asset existence
    - Provide asset URLs/paths
    """

    def __init__(
        self,
        asset_directory: str | Path,
    ) -> None:
        self.asset_directory = Path(asset_directory)

    #################################################################
    # Public API
    #################################################################

    def css(self, filename: str = "report.css") -> Path:
        """
        Return CSS asset path.
        """
        return self._resolve("css", filename)

    def javascript(
        self,
        filename: str = "report.js",
    ) -> Path:
        """
        Return JavaScript asset path.
        """
        return self._resolve("js", filename)

    def image(
        self,
        filename: str,
    ) -> Path:
        """
        Return image asset path.
        """
        return self._resolve("images", filename)

    #################################################################
    # Internal Helpers
    #################################################################

    def _resolve(
        self,
        category: str,
        filename: str,
    ) -> Path:
        """
        Resolve an asset path.

        Raises
        ------
        FileNotFoundError
            If the requested asset does not exist.
        """

        path = self.asset_directory / category / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Asset not found: {path}"
            )

        return path