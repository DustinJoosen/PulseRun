from enum import Enum


class ScreenCodes(Enum):
    MA = 1,     # Main screen
    SH = 2,     # Shop
    BA = 3      # Battle


class ProjectileOrigin(Enum):
    Player = 0,
    Enemy = 1
