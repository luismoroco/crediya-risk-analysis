from domain import ApplicationStatus


def test_enum_members():
    assert ApplicationStatus.REJECTED.name == "REJECTED"
    assert ApplicationStatus.PENDING.name == "PENDING"
    assert ApplicationStatus.MANUAL_REVIEW.name == "MANUAL_REVIEW"
    assert ApplicationStatus.APPROVED.name == "APPROVED"

    assert ApplicationStatus.REJECTED.value == 1
    assert ApplicationStatus.PENDING.value == 2
    assert ApplicationStatus.MANUAL_REVIEW.value == 3
    assert ApplicationStatus.APPROVED.value == 4


def test_enum_lookup_by_name():
    assert ApplicationStatus["APPROVED"] == ApplicationStatus.APPROVED
    assert ApplicationStatus["REJECTED"] == ApplicationStatus.REJECTED


def test_enum_lookup_by_value():
    assert ApplicationStatus(1) == ApplicationStatus.REJECTED
    assert ApplicationStatus(4) == ApplicationStatus.APPROVED
