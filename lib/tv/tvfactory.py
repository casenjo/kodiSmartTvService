from sony import TvSony


class TvFactory:

    def __init__(self):
        self.availableTvs = dict(Sony=TvSony)

    def getTv(self, tv=None):
        return self.availableTvs[tv]()