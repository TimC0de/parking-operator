import os


def env_param(name: str) -> str:
    """Get env variable value."""
    value = os.environ.get(name)

    if value:
        return value

    raise EnvironmentError(f'Required environment variable "{name}" is missing')


def env_optional_param(name: str) -> str | None:
    return os.environ.get(name, None)