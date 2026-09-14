"""Domain-separated fingerprints and fail-closed integrity verification."""

import hashlib
import hmac
import re
from dataclasses import dataclass
from enum import StrEnum

from ai_quant_lab.core.codec import GovernedRecord, encode

_FINGERPRINT = re.compile(r"^sha256:[0-9a-f]{64}$")


class IntegrityError(ValueError):
    """Base error for integrity-contract failures."""


class InvalidFingerprint(IntegrityError):
    pass


class IntegrityMismatch(IntegrityError):
    pass


class IntegrityStatus(StrEnum):
    VERIFIED = "VERIFIED"


@dataclass(frozen=True, slots=True)
class IntegrityVerification:
    status: IntegrityStatus
    actual_fingerprint: str


def fingerprint_record(record: GovernedRecord) -> str:
    """Fingerprint canonical typed bytes; the encoded type provides domain separation."""
    return "sha256:" + hashlib.sha256(encode(record)).hexdigest()


def verify_integrity(record: GovernedRecord, expected_fingerprint: str) -> IntegrityVerification:
    if not isinstance(expected_fingerprint, str) or not _FINGERPRINT.fullmatch(
        expected_fingerprint
    ):
        raise InvalidFingerprint("expected fingerprint must be canonical SHA-256")
    actual = fingerprint_record(record)
    if not hmac.compare_digest(actual, expected_fingerprint):
        raise IntegrityMismatch("canonical content does not match expected fingerprint")
    return IntegrityVerification(IntegrityStatus.VERIFIED, actual)
