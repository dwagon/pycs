""" Utility functions """


def check_args(valid, cname, kwargs):
    """Check that the kwargs are in the permitted list"""
    for arg in kwargs:
        assert arg in valid, f"{cname}: {arg} not in {valid}"


# EOF
