from enum import Enum


class Exchange(Enum):
    UNKNOWN = 0,
    SHSE = 1,
    SZSE = 2,
    CFFEX = 3,
    SHFE = 4,
    DCE = 5,
    CZCE = 6,
    INE = 7,
    SGE = 8,
    HKEX = 9,
    # 一些转换方法

    def __str__(self):
        return self.name


def exchange_transform(ex):
    if ex == 'SZ':
        ex = 'SZSE'
    elif ex == 'SH':
        ex = 'SHSE'
    else:
        pass
    return ex


class Code:
    """
    Code class.
    """

    def __init__(self, code=None, symbol=None, exchange=None, **kwargs):
        # 解析code, symbol, exchange
        if code is None:
            if symbol is not None and exchange is not None:
                self.symbol = symbol
                self.exchange = Exchange[exchange]
                self.code = "%s.%s" % (self.symbol, self.exchange)
            else:
                raise ValueError((code, symbol, exchange))
        else:
            if symbol is not None and exchange is not None:
                self.code = code
                self.symbol = symbol
                self.exchange = Exchange[exchange]
            else:
                self.code = code
                # 根据历史上约定code格式进行解析
                self.symbol = code.split(".")[0]
                self.exchange = Exchange[exchange_transform(code.split(".")[1])]
        self.__info = kwargs
        assert (set(self.__info.keys()) <= set(["codetype", 'optiontype', 'underlying', 'strike_price', 'expire_date']))

    def get(self, key):
        return self.__info.get(key)

    def __str__(self):
        return "%s.%s" % (self.symbol, self.exchange)

    def __hash__(self):
        value = hash(self.code) + hash(self.symbol) + hash(self.exchange)
        for key, values in self.__info.items():
            value += hash(key)
            value += hash(values)
        return value

    def __eq__(self, others):
        return (self.code == others.code) and (self.symbol == others.symbol) and (self.exchange == others.exchange) and (self.__info == others.__info)

    def __gt__(self, other):
        # 重载大于运算符
        return self.code > other.code

    def __lt__(self, other):
        # 重载小于运算符
        return self.code < other.code

