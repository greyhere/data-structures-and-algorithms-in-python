''' C-2.30
At the close of Section 2.4.1, we suggest a model in which the CreditCard
class supports a nonpublic method, _set_balance(b), that could be used
by subclasses to affect a change to the balance, without directly accessing
the _balance data member. Implement such a model, revising both the
CreditCard and PredatoryCreditCard classes accordingly.
'''

class CreditCard:
    def __init__(self, customer, bank, acnt, limit, balance=0):
        self._customer = customer
        self._bank = bank
        self._account = acnt
        self._limit = limit
        self._balance = balance
    
    def get_customer(self):
        return self._customer
    
    def get_bank(self):
        return self._bank
    
    def get_account(self):
        return self._account
    
    def get_limit(self):
        return self._limit
    
    def get_balance(self):
        return self._balance
    
    def _set_balance(self, b):
        self._balance = b
    
    def charge(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError('Price must be a number.')
        elif price + self._balance > self._limit:
            return False
        else:
            self._balance += price
            return True
    
    def make_payment(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError('Amount must be a number.')
        elif amount < 0:
            raise ValueError('Amount cannot be negative.')
        else:
            self._balance -= amount


class PredatoryCreditCard(CreditCard):
    MAX_CHARGES = 10
    LATE_FEE = 10
    MIN_PCT = 0.4
    
    def __init__(self, customer, bank, acnt, limit, apr):
        super().__init__(customer, bank, acnt, limit)
        self._apr = apr
        self._charge_count = 0
        self._min_payment = 0
    
    def charge(self, price):
        success = super().charge(price)
        if not success:
            super()._set_balance(super().get_balance() + 5)
        else:
            self._charge_count += 1
            if self._charge_count > PredatoryCreditCard.MAX_CHARGES:
                super()._set_balance(super().get_balance() + 1)
        return success
    
    def make_payment(self, amount):
        super().make_payment(amount)
        self._min_payment = max(0, self._min_payment - amount)
    
    def process_month(self):
        if self._min_payment > 0:
            super()._set_balance(super().get_balance() + PredatoryCreditCard.LATE_FEE)
        if super().get_balance() > 0:
            monthly_factor = pow(1+self._apr, 1/12)
            super()._set_balance(super().get_balance() * monthly_factor)
            self._min_payment = round(PredatoryCreditCard.MIN_PCT*super().get_balance(), 2)
        self._charge_count = 0


if __name__ == '__main__':
    wallet = PredatoryCreditCard('John Bowman', 'California Savings', '5391 0375 9387 5309', 2500, 8)
    
    for val in range(15):
        wallet.charge(100)
    
    wallet.process_month()
    print('Balance =', wallet.get_balance())
    print('Minimum payment =', wallet._min_payment)
    
    wallet.make_payment(800)
    print('\nBalance =', wallet.get_balance())
    print('Minimum payment =', wallet._min_payment)
    
    wallet.process_month()
    print('\nBalance =', wallet.get_balance())
    print('Minimum payment =', wallet._min_payment)
