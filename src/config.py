import json
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

MIN_LEVELS = 10
MAX_LEVELS = 100
MIN_MAZE_SIDE = 7
MAX_MAZE_SIDE = 50
DEFAULT_HIGHSCORE_FILENAME = "highscores.json"

KNOWN_KEYS = (
    "highscore_filename",
    "level",
    "lives",
    "pacgum",
    "points_per_pacgum",
    "points_per_super_pacgum",
    "points_per_ghost",
    "seed",
    "level_max_time",
)


class ConfigError(Exception):
    """Raised when the configuration file can't be used at all."""


@dataclass(frozen=True)
class LevelConfig:
    """Size of one level's maze, in cells.

    Attributes:
        width: Cells from left to right.
        height: Cells from top to bottom.
    """

    width: int
    height: int


DEFAULT_LEVELS = tuple(
    LevelConfig(15 + index, 15 + index) for index in range(MIN_LEVELS)
)


@dataclass(frozen=True)
class GameConfig:
    """Validated game settings.

    Attributes:
        highscore_filename: File where highscores are saved.
        levels: Levels in play order.
        lives: Lives at the start of a game.
        pacgum: Pacgums placed in each level.
        points_per_pacgum: Points for a pacgum.
        points_per_super_pacgum: Points for a super-pacgum.
        points_per_ghost: Points for an edible ghost.
        seed: Seed of the first level's maze.
        level_max_time: Time limit per level, in seconds.
    """

    highscore_filename: str
    levels: tuple[LevelConfig, ...]
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int


def load_config(path: str) -> GameConfig:
    """Read, parse and validate the configuration file.

    Args:
        path: Path of the JSON config file.

    Returns:
        The settings, with bad values replaced or clamped.

    Raises:
        ConfigError: If the file can't be read or parsed.
    """
    data = read_config_file(path)
    for key in data:
        if key not in KNOWN_KEYS:
            logger.warning("config: unknown key '%s' ignored", key)
    return GameConfig(
        highscore_filename=read_filename(data),
        levels=read_levels(data),
        lives=read_int(data, "lives", default=3, low=1, high=10),
        pacgum=read_int(data, "pacgum", default=42, low=1, high=2500),
        points_per_pacgum=read_int(
            data, "points_per_pacgum", default=10, low=0, high=100_000
        ),
        points_per_super_pacgum=read_int(
            data, "points_per_super_pacgum", default=50, low=0, high=100_000
        ),
        points_per_ghost=read_int(
            data, "points_per_ghost", default=200, low=0, high=100_000
        ),
        seed=read_int(data, "seed", default=42, low=1, high=2**31 - 1),
        level_max_time=read_int(
            data, "level_max_time", default=90, low=10, high=3600
        ),
    )


def read_config_file(path: str) -> dict[str, Any]:
    """Read the file and parse it as JSON with comment lines.

    Args:
        path: Path of the JSON config file.

    Returns:
        The top-level JSON object.

    Raises:
        ConfigError: If the file can't be read, isn't valid JSON, or isn't
            a JSON object.
    """
    try:
        with open(path, encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        raise ConfigError(f"config file '{path}' does not exist")
    except IsADirectoryError:
        raise ConfigError(f"'{path}' is a directory, not a config file")
    except PermissionError:
        raise ConfigError(f"no permission to read config file '{path}'")
    except UnicodeDecodeError:
        raise ConfigError(f"config file '{path}' is not UTF-8 text")
    except OSError as error:
        raise ConfigError(f"can't read config file '{path}': {error}")

    try:
        data = json.loads(strip_comments(text))
    except json.JSONDecodeError as error:
        raise ConfigError(
            f"config file '{path}' is not valid JSON: {error.msg} "
            f"(line {error.lineno}, column {error.colno})"
        )
    if not isinstance(data, dict):
        raise ConfigError(
            f"config file '{path}' must contain a JSON object: {{ ... }}"
        )
    return data


def strip_comments(text: str) -> str:
    """Empty the lines that start with '#' or '//'.

    Lines are emptied, not removed, so JSON error line numbers still match
    the file.

    Args:
        text: Content of the config file.

    Returns:
        The text without comments.
    """
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith("//"):
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def read_int(
    data: dict[str, Any],
    key: str,
    default: int,
    low: int,
    high: int,
    label: str = "",
) -> int:
    """Return data[key] clamped to [low, high], or default if invalid.

    Args:
        data: JSON object to read from.
        key: Key of the value.
        default: Used when the value is missing or not a whole number.
        low: Smallest allowed value.
        high: Largest allowed value.
        label: Name used in warnings. Defaults to the key.

    Returns:
        A valid value. Every correction is logged.
    """
    name = label or f"'{key}'"
    if key not in data:
        logger.warning("config: %s is missing, using %d", name, default)
        return default
    value = data[key]
    # bool is a subclass of int in Python, so `true` would pass as 1.
    if isinstance(value, bool) or not isinstance(value, int):
        logger.warning(
            "config: %s must be a whole number, not %s; using %d",
            name,
            json.dumps(value),
            default,
        )
        return default
    if value < low or value > high:
        clamped = min(max(value, low), high)
        logger.warning(
            "config: %s = %d is outside %d..%d; using %d",
            name,
            value,
            low,
            high,
            clamped,
        )
        return clamped
    return value


def read_filename(data: dict[str, Any]) -> str:
    """Return the highscore file name, or the default if invalid.

    Args:
        data: Top-level JSON object.

    Returns:
        A non-empty file name.
    """
    key = "highscore_filename"
    if key not in data:
        logger.warning(
            "config: '%s' is missing, using '%s'",
            key,
            DEFAULT_HIGHSCORE_FILENAME,
        )
        return DEFAULT_HIGHSCORE_FILENAME
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        logger.warning(
            "config: '%s' must be a non-empty string, not %s; using '%s'",
            key,
            json.dumps(value),
            DEFAULT_HIGHSCORE_FILENAME,
        )
        return DEFAULT_HIGHSCORE_FILENAME
    return value.strip()


def read_levels(data: dict[str, Any]) -> tuple[LevelConfig, ...]:
    """Return the levels, completed to MIN_LEVELS and cut to MAX_LEVELS.

    Args:
        data: Top-level JSON object.

    Returns:
        Valid levels.
    """
    if "level" not in data:
        logger.warning("config: 'level' is missing, using default levels")
        return DEFAULT_LEVELS
    entries = data["level"]
    if not isinstance(entries, list) or not entries:
        logger.warning(
            "config: 'level' must be a non-empty list, using default levels"
        )
        return DEFAULT_LEVELS
    if len(entries) > MAX_LEVELS:
        logger.warning(
            "config: %d levels given, keeping the first %d",
            len(entries),
            MAX_LEVELS,
        )
        entries = entries[:MAX_LEVELS]

    levels = [
        read_level(entry, number)
        for number, entry in enumerate(entries, start=1)
    ]
    if len(levels) < MIN_LEVELS:
        logger.warning(
            "config: only %d levels given, at least %d are needed; "
            "adding default levels %d to %d",
            len(levels),
            MIN_LEVELS,
            len(levels) + 1,
            MIN_LEVELS,
        )
        levels.extend(DEFAULT_LEVELS[len(levels):])
    return tuple(levels)


def read_level(entry: Any, number: int) -> LevelConfig:
    """Return one level, using defaults for a bad entry or value.

    Args:
        entry: Value from the 'level' list.
        number: Position of the level, starting at 1.

    Returns:
        A level with a valid width and height.
    """
    default = DEFAULT_LEVELS[min(number, MIN_LEVELS) - 1]
    if not isinstance(entry, dict):
        logger.warning(
            "config: level %d must be an object like "
            '{"width": 15, "height": 15}; using %dx%d',
            number,
            default.width,
            default.height,
        )
        return default
    for key in entry:
        if key not in ("width", "height"):
            logger.warning(
                "config: unknown key '%s' in level %d ignored", key, number
            )
    width = read_int(
        entry,
        "width",
        default.width,
        MIN_MAZE_SIDE,
        MAX_MAZE_SIDE,
        label=f"level {number} 'width'",
    )
    height = read_int(
        entry,
        "height",
        default.height,
        MIN_MAZE_SIDE,
        MAX_MAZE_SIDE,
        label=f"level {number} 'height'",
    )
    return LevelConfig(width, height)
