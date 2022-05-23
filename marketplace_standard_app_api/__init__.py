"""Materials-MarketPlace Standard App API

Authors:
  - Simon Adorf <simon.adorf@epfl.ch>

This package defines the standard app API for the Materials Marketplace.  It is
used to both template MarketPlace applications and lint their published APIs
during the registration process.
"""

from .main import api
from .version import __version__

__all__ = ["api", "__version__"]
