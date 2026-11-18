import logging
import sys

from src.config import ConfigError, load_config

USAGE = "usage: python3 pac-man.py <config.json>"


def main(args: list[str]) -> int:
    """Start the game with the configuration file given on the command line.

    Args:
        args: Command-line arguments, without the program name.

    Returns:
        The exit status: 0 on success, 1 on error.
    """
    logging.basicConfig(format="%(levelname)s: %(message)s")
    if len(args) != 1:
        print(
            f"Error: expected exactly one argument, got {len(args)}\n{USAGE}",
            file=sys.stderr,
        )
        return 1
    try:
        config = load_config(args[0])
    except ConfigError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    sizes = ", ".join(f"{lvl.width}x{lvl.height}" for lvl in config.levels)
    print(f"Config loaded: {config.lives} lives, levels {sizes}")
    # TODO: start the game here once it exists.
    return 0


if __name__ == "__main__":
    # Last line of defence: the subject forbids showing a traceback.
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as error:
        print(f"Unexpected error: {error}", file=sys.stderr)
        sys.exit(1)
