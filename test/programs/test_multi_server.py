import typing
import unittest
from MultiServer import Context, LimitExceeded, ServerCommandProcessor, compute_value


class TestResolvePlayerName(unittest.TestCase):
    def test_resolve(self) -> None:
        p = ServerCommandProcessor(Context("", 0, "", "", 0, 0, False))
        p.ctx.player_names = {
            (1, 1): "AAA",
            (1, 2): "aBc",
            (1, 3): "abC",
        }
        assert not p.resolve_player("abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("aBc") == (1, 2, "aBc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"
        assert not p.resolve_player("abCD"), "incorrect name shouldn't resolve to player"

        p.ctx.player_names = {
            (1, 1): "aaa",
            (1, 2): "abc",
            (1, 3): "abC",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("aBc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"

        p.ctx.player_names = {
            (1, 1): "AbcdE",
            (1, 2): "abc",
            (1, 3): "abCD",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("Abc") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("ABC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("abcd") == (1, 3, "abCD"), "case insensitive resolves when 1 match"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"

DataStorageOp = typing.Callable[[typing.Any, typing.Any], typing.Any]

class TestDataStorageOperations(unittest.TestCase):

    def test_modulo_string_any(self):
        ctx = Context("", 0, "", "", 0, 0, False)

        assert ctx.disable_string_modulo == True

        op_mod: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "mod", lhs, rhs)

        self.assertRaises(ValueError, lambda: op_mod("%s", None));
        self.assertRaises(ValueError, lambda: op_mod("%s", 0));
        self.assertRaises(ValueError, lambda: op_mod("%s", 0.0));
        self.assertRaises(ValueError, lambda: op_mod("%s", ""));
        self.assertRaises(ValueError, lambda: op_mod("%s", []));
        self.assertRaises(ValueError, lambda: op_mod("%s", {}));
        self.assertRaises(ValueError, lambda: op_mod("%s", object()));

    def test_add_int_int(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_add: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "add", lhs, rhs)
        max_int_bits = ctx.limits["max_int_bits"].value
        max_int = 2 ** max_int_bits - 1
        min_int = -max_int

        result = op_add(max_int, 0)
        assert result == max_int
        assert result.bit_length() <= max_int_bits

        result = op_add(min_int, 0)
        assert result == min_int
        assert result.bit_length() <= max_int_bits

        self.assertRaises(LimitExceeded, lambda: op_add(max_int, 1))
        self.assertRaises(LimitExceeded, lambda: op_add(min_int, -1))

    def test_add_str_str(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_add: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "add", lhs, rhs)
        max_str_len = ctx.limits["max_string_len"].value
        max_str = "a" * max_str_len

        result = op_add(max_str, "")
        assert result == max_str
        assert len(result) <= max_str_len

        result = op_add("abc", "def")
        assert result == "abcdef"
        assert len(result) <= max_str_len

        self.assertRaises(LimitExceeded, lambda: op_add(max_str, "a"))

    def test_add_list_list(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_add: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "add", lhs, rhs)
        max_list_len = ctx.limits["max_list_len"].value
        max_list = ["a"] * max_list_len

        result = op_add(max_list, [])
        assert result == max_list
        assert len(result) <= max_list_len

        result = op_add(["abc"], ["def"])
        assert result == ["abc", "def"]
        assert len(result) <= max_list_len

        self.assertRaises(LimitExceeded, lambda: op_add(max_list, ["a"]))

    def test_mul_int_int(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_mul: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "mul", lhs, rhs)
        max_int_bits = ctx.limits["max_int_bits"].value
        max_int = 2 ** max_int_bits - 1
        min_int = -max_int

        result = op_mul(0, 0)
        assert result == 0

        result = op_mul(0, max_int + 1)
        assert result == 0

        result = op_mul(max_int + 1, 0)
        assert result == 0

        result = op_mul(1, max_int)
        assert result == max_int

        result = op_mul(max_int, 1)
        assert result == max_int

        result = op_mul(max_int // 15, 15)
        assert result == max_int

        result = op_mul(15, max_int // 15)
        assert result == max_int

        self.assertRaises(LimitExceeded, lambda: op_mul(max_int // 15, 16))
        self.assertRaises(LimitExceeded, lambda: op_mul(16, max_int // 15))

        result = op_mul(0, min_int - 1)
        assert result == 0

        result = op_mul(min_int - 1, 0)
        assert result == 0

        result = op_mul(1, min_int)
        assert result == min_int

        result = op_mul(min_int, 1)
        assert result == min_int

        result = op_mul(min_int // 15, 15)
        assert result == min_int

        result = op_mul(15, min_int // 15)
        assert result == min_int

        self.assertRaises(LimitExceeded, lambda: op_mul(min_int // 15, 16))
        self.assertRaises(LimitExceeded, lambda: op_mul(16, min_int // 15))

    def test_mul_str_int(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_mul: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "mul", lhs, rhs)
        max_str_len = ctx.limits["max_string_len"].value
        max_str = "a" * max_str_len

        result = op_mul("a", max_str_len)
        assert result == max_str

        self.assertRaises(LimitExceeded, lambda: op_mul("a", max_str_len + 1))

    def test_mul_int_str(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_mul: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "mul", lhs, rhs)
        max_str_len = ctx.limits["max_string_len"].value
        max_str = "a" * max_str_len

        result = op_mul(max_str_len, "a")
        assert result == max_str

        self.assertRaises(LimitExceeded, lambda: op_mul(max_str_len + 1, "a"))

    def test_mul_list_int(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_mul: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "mul", lhs, rhs)
        max_list_len = ctx.limits["max_list_len"].value
        max_list = ["a"] * max_list_len

        result = op_mul(["a"], max_list_len)
        assert result == max_list

        self.assertRaises(LimitExceeded, lambda: op_mul(["a"], max_list_len + 1))

    def test_mul_int_list(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_mul: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "mul", lhs, rhs)
        max_list_len = ctx.limits["max_list_len"].value
        max_list = ["a"] * max_list_len

        result = op_mul(max_list_len, ["a"])
        assert result == max_list

        self.assertRaises(LimitExceeded, lambda: op_mul(max_list_len + 1, ["a"]))

    def test_pow_int_int(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_pow: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "pow", lhs, rhs)
        max_int_bits = ctx.limits["max_int_bits"].value
        max_int = 2 ** max_int_bits - 1
        min_int = -max_int

        result = op_pow(0, 0)
        assert result == 1

        result = op_pow(0, max_int + 1)
        assert result == 0

        result = op_pow(max_int + 1, 0)
        assert result == 1

        result = op_pow(1, max_int_bits)
        assert result == 1

        result = op_pow(2, max_int_bits - 1)
        assert result == 2 ** (max_int_bits - 1)

        self.assertRaises(LimitExceeded, lambda: op_pow(2, max_int_bits))

        result = op_pow(min_int - 1, 0)
        assert result == 1

        result = op_pow(-1, max_int_bits)
        assert result == 1

        result = op_pow(-2, max_int_bits - 1)
        assert result == (-2) ** (max_int_bits - 1)

        self.assertRaises(LimitExceeded, lambda: op_pow(-2, max_int_bits))

    def test_lshift_int_int(self):
        ctx = Context("", 0, "", "", 0, 0, False)
        op_lshift: DataStorageOp = lambda lhs, rhs: compute_value(ctx, "left_shift", lhs, rhs)
        max_int_bits = ctx.limits["max_int_bits"].value
        max_int = 2 ** max_int_bits - 1

        result = op_lshift(0, 0)
        assert result == 0

        result = op_lshift(0, max_int)
        assert result == 0

        result = op_lshift(1, max_int_bits - 1)
        assert result == 1 << (max_int_bits - 1)

        self.assertRaises(LimitExceeded, lambda: op_lshift(1, max_int_bits))
