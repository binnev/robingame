from packaging.version import Version as _Version


class Version(_Version):
    notes: list[str]

    def __init__(self, version: str, notes=None) -> None:
        super().__init__(version)
        self.notes = notes or []


VERSION_0_0_1 = Version(notes=["Initial version."])
