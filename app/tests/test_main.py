import pytest
import main

def test_main():
    result = main()
    assert result == 0
