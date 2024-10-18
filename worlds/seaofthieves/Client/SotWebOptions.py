class SotWebOptions:
    def __init__(self):

        self.forceBlockAllOverride: bool = False

        self._allowBalanceQuery: bool = False
        self._allowCaptainQuery: bool = False

    def setQueries(self, value: bool):
        self.allowBalanceQuery = value
        self.allowCaptainQuery = value

    @property
    def allowBalanceQuery(self):
        if self.forceBlockAllOverride:
            return False
        return self._allowBalanceQuery

    @allowBalanceQuery.setter
    def allowBalanceQuery(self, value: bool):
        self._allowBalanceQuery = value

    @property
    def allowCaptainQuery(self):
        if self.forceBlockAllOverride:
            return False
        return self._allowCaptainQuery

    @allowCaptainQuery.setter
    def allowCaptainQuery(self, value: bool):
        self._allowCaptainQuery = value
