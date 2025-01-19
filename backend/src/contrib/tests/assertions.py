import re


def is_valid_sha256(string: str) -> bool:
    sha256_pattern = re.fullmatch(pattern=r'[a-fA-F0-9]{64}', string=string)

    return bool(sha256_pattern)
