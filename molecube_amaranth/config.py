#

from dataclasses import dataclass

from . import io

# Change this version when making backward incompatible changes.
MAJOR_VERSION = 5
# Change this version when adding new features
MINOR_VERSION = 4

@dataclass(kw_only=True)
class Config:
    TTLIN: str = ''
    TTLOUT: str = ' '.join(io.ttl_bd_pin(fmc, idx) for fmc in range(2) for idx in range(28))
    CLOCKOUT: str = io.sma_pin(1, 0)

    SPI_MISO: str = ''
    SPI_MOSI: str = ''
    SPI_SCLK: str = ''
    SPI_CS: str = ''

    CLOCK_HZ: float = 200e6
    CLOCK_SHIFT: int = 1
