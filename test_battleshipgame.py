from game_engine import Testing_GridA  # Import GridA from the appropriate module

def test_check_GridA():
    tester  = Testing_GridA()
    tester.ship_add("1")
    assert tester.ship_size() == 1

