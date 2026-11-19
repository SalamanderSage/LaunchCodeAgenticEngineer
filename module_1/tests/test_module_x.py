"""Unit tests for module_x public functions."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from module_x import (  # noqa: E402
    VALID_CUSTOMER_TIERS,
    calculate_discount,
    classify_priority,
    is_valid_project_code,
    normalize_name,
    summarize_order,
)


# --- normalize_name ---------------------------------------------------------

class TestNormalizeName:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("alice", "Alice"),
            ("  alice   smith  ", "Alice Smith"),
            ("ALICE SMITH", "Alice Smith"),
            ("alice\t\nsmith", "Alice Smith"),
            ("mary jane watson", "Mary Jane Watson"),
        ],
    )
    def test_normalizes(self, raw, expected):
        assert normalize_name(raw) == expected

    @pytest.mark.parametrize("raw", ["", "   ", "\t\n"])
    def test_empty_raises_value_error(self, raw):
        with pytest.raises(ValueError, match="cannot be empty"):
            normalize_name(raw)

    @pytest.mark.parametrize("raw", [None, 123, ["alice"]])
    def test_non_string_raises_type_error(self, raw):
        with pytest.raises(TypeError, match="must be a string"):
            normalize_name(raw)


# --- calculate_discount -----------------------------------------------------

class TestCalculateDiscount:
    @pytest.mark.parametrize(
        "tier, expected",
        [
            ("standard", 100.00),
            ("silver", 95.00),
            ("gold", 90.00),
            ("platinum", 85.00),
        ],
    )
    def test_each_tier(self, tier, expected):
        assert calculate_discount(100, tier) == expected

    def test_all_valid_tiers_covered(self):
        assert VALID_CUSTOMER_TIERS == {"standard", "silver", "gold", "platinum"}

    @pytest.mark.parametrize("tier", ["  GOLD  ", "Gold", "gOlD"])
    def test_tier_is_case_and_whitespace_insensitive(self, tier):
        assert calculate_discount(100, tier) == 90.00

    def test_rounds_to_two_decimals(self):
        # 19.99 * 0.95 = 18.9905
        assert calculate_discount(19.99, "silver") == 18.99

    def test_zero_price(self):
        assert calculate_discount(0, "platinum") == 0.0

    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            calculate_discount(-0.01, "gold")

    def test_unknown_tier_raises(self):
        with pytest.raises(ValueError, match="unknown customer tier: bronze"):
            calculate_discount(100, "bronze")


# --- classify_priority ------------------------------------------------------

class TestClassifyPriority:
    @pytest.mark.parametrize(
        "score, expected",
        [
            (0, "low"),
            (39, "low"),
            (40, "medium"),
            (69, "medium"),
            (70, "high"),
            (89, "high"),
            (90, "urgent"),
            (100, "urgent"),
        ],
    )
    def test_boundaries(self, score, expected):
        assert classify_priority(score) == expected

    @pytest.mark.parametrize("score", [-1, 101])
    def test_out_of_range_raises(self, score):
        with pytest.raises(ValueError, match="between 0 and 100"):
            classify_priority(score)

    @pytest.mark.parametrize("score", [50.0, "50", None])
    def test_non_int_raises(self, score):
        with pytest.raises(TypeError, match="must be an integer"):
            classify_priority(score)


# --- summarize_order --------------------------------------------------------

class TestSummarizeOrder:
    @pytest.mark.parametrize("items", [[], None])
    def test_empty(self, items):
        assert summarize_order(items) == {"item_count": 0, "subtotal": 0.0}

    def test_single_item(self):
        result = summarize_order([{"quantity": 3, "unit_price": 2.5}])
        assert result == {"item_count": 3, "subtotal": 7.5}

    def test_multiple_items(self):
        items = [
            {"name": "pen", "quantity": 2, "unit_price": 1.25},
            {"name": "pad", "quantity": 1, "unit_price": 4},
        ]
        assert summarize_order(items) == {"item_count": 3, "subtotal": 6.5}

    def test_subtotal_rounded(self):
        result = summarize_order([{"quantity": 3, "unit_price": 0.1}])
        assert result["subtotal"] == 0.3

    def test_missing_keys_default_to_zero(self):
        assert summarize_order([{}]) == {"item_count": 0, "subtotal": 0.0}

    def test_zero_quantity(self):
        result = summarize_order([{"quantity": 0, "unit_price": 9.99}])
        assert result == {"item_count": 0, "subtotal": 0.0}

    @pytest.mark.parametrize("quantity", [-1, 1.5, "2"])
    def test_invalid_quantity_raises(self, quantity):
        with pytest.raises(ValueError, match="quantity"):
            summarize_order([{"quantity": quantity, "unit_price": 1.0}])

    @pytest.mark.parametrize("unit_price", [-0.01, "1.00", None])
    def test_invalid_unit_price_raises(self, unit_price):
        with pytest.raises(ValueError, match="unit_price"):
            summarize_order([{"quantity": 1, "unit_price": unit_price}])


# --- is_valid_project_code --------------------------------------------------

class TestIsValidProjectCode:
    @pytest.mark.parametrize("code", ["AB-1234", "ZZ-0000", "QX-9999"])
    def test_valid(self, code):
        assert is_valid_project_code(code) is True

    @pytest.mark.parametrize(
        "code",
        [
            "",
            "AB1234",       # no separator
            "AB-12-34",     # too many parts
            "ab-1234",      # lowercase prefix
            "Ab-1234",      # mixed-case prefix
            "A-1234",       # prefix too short
            "ABC-1234",     # prefix too long
            "A1-1234",      # non-alpha prefix
            "AB-123",       # number too short
            "AB-12345",     # number too long
            "AB-12a4",      # non-digit number
            " AB-1234",     # leading whitespace
        ],
    )
    def test_invalid(self, code):
        assert is_valid_project_code(code) is False

    @pytest.mark.parametrize("code", [None, 1234, ["AB", "1234"]])
    def test_non_string_returns_false(self, code):
        assert is_valid_project_code(code) is False
