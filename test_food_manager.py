from food_manager import FoodQueue

def test_add_order():
    q = FoodQueue()
    q.add_order("Bún chả")
    assert len(q.orders) == 1
    assert q.orders[0] == "Bún chả"

def test_process_order():
    q = FoodQueue()
    q.add_order("Cơm rang")
    q.process_order()
    assert len(q.orders) == 0