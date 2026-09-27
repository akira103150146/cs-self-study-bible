import pytest

from checklib import (bits_for, f32_bits, f32_fields, f32_from_bits, from_base, from_twos,
                      huffman_bits, image_bytes, ones, pcm_bytes, rle, signmag, to_base, twos,
                      utf8_hex)


def test_bases():
    assert to_base(255, 16) == "ff" and to_base(0, 2) == "0" and from_base("777", 8) == 511
    assert to_base(35, 36) == "z"


def test_signed():
    assert twos(-37, 8) == "11011011" and ones(-37, 8) == "11011010" and signmag(-37, 8) == "10100101"
    assert twos(-128, 8) == "10000000" and from_twos("11011011") == -37 and from_twos("0101") == 5
    with pytest.raises(ValueError):
        twos(128, 8)
    with pytest.raises(ValueError):
        ones(-128, 8)


def test_float():
    assert f32_bits(-6.25) == "11000000110010000000000000000000"
    assert f32_fields(1.0) == (0, 127, 0)
    assert f32_from_bits("0" * 31 + "1") == pytest.approx(1.401298464324817e-45)


def test_text_and_media():
    assert utf8_hex("中") == "E4 B8 AD" and utf8_hex("😀") == "F0 9F 98 80" and utf8_hex("A") == "41"
    assert rle("AAAAAAAAAAAB") == "*A9AAB" and rle("BBBBB") == "*B5" and rle("CCC") == "CCC"
    assert rle("D" * 13) == "*D9*D4"
    with pytest.raises(ValueError):
        rle("a*b")
    assert huffman_bits({"A": 5, "B": 2, "C": 1, "D": 1}) == 15
    assert huffman_bits({"A": 7}) == 7
    assert pcm_bytes(44100, 16, 2, 1) == 176400 and image_bytes(1920, 1080, 24) == 6220800
    assert bits_for(1) == 1 and bits_for(2) == 1 and bits_for(5) == 3 and bits_for(256) == 8
