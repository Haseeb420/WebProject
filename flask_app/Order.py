
class Order:
    def __init__(self,order_id,user_id,province,city,town,address,prod_id,prod_price,shipping_fee,total,date):
        self.order_id=order_id
        self.user_id=user_id
        self.province=province
        self.city=city
        self.town=town
        self.address=address
        self.prod_id=prod_id
        self.prod_price=prod_price
        self.shipping_fee=shipping_fee
        self.total=total
        self.date=date