""" Utility functions """


from typing import Any


def check_args(valid: set[str], cname: str, kwargs: dict[str, Any]) -> None:
    """Check that the kwargs are in the permitted list"""
    for arg in kwargs:
        assert arg in valid, f"{cname}: '{arg}' not in {valid}"


# EOF
