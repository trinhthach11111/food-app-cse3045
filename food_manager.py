class FoodQueue:
    def __init__(self):
        self.orders = []

    def add_order(self, item_name):
        self.orders.append(item_name)
        print(f"Đã thêm đơn hàng: {item_name}")

    def process_order(self):
        if self.orders:
            completed = self.orders.pop(0)
            print(f"Đã xử lý xong đơn: {completed}")

if __name__ == "__main__":
    q = FoodQueue()
    q.add_order("Mì tôm xào bò")
    q.add_order("Cơm rang dưa bò")
    q.process_order()