from Target import Target


class Deer(Target):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hasbtv = False
        self.numbites = 0

    def isbitten(self, midge):
        if midge.hasbtv:
            self.hasbtv = True
        elif self.hasbtv:
            midge.hasbtv = True

        self.numbites += 1

    def feed(self, midge):
        self.isbitten(midge)
        midge.fed = True
        midge.timesincefed = 0

    def step(self):
        # print("By day " + str(self.model.day) + ", deer " + str(self.unique_id) + " was bitten " + str(self.numbites) + " times.")
        return