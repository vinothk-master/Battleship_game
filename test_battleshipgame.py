from game_engine import Testing_GridA # Import GridA from the appropriate module
#This code to test Battleship game 
def test_checking_GridA():
    tester  = Testing_GridA()
    tester.ship_add("1")
    print("Executing the test line")
    assert tester.ship_size() == 1

