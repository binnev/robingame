from packaging.version import Version as _Version


class Version(_Version):
    notes: list[str]

    def __init__(self, version: str, notes=None) -> None:
        super().__init__(version)
        self.notes = notes or []


VERSION_0_0_13 = Version(notes=["Corrected typing on ease functions."])
VERSION_0_0_12 = Version(notes=["Fixed broken ; character in cellphone font"])
VERSION_0_0_11 = Version(
    notes=["@record decorator now allows you to specify number of processes for async image saving"]
)
VERSION_0_0_10 = Version(notes=["Fixed broken imports (again)."])
VERSION_0_0_9 = Version(notes=["Fixed broken imports."])
VERSION_0_0_8 = Version(notes=["Added GameCube controller input visualizer."])
VERSION_0_0_7 = Version(
    notes=["Modified animation ease functions so they generate a single value, not a whole array."]
)
VERSION_0_0_6 = Version(
    notes=["Fixed a bug in InputQueue due to the way pygame stores keyboard presses."]
)
VERSION_0_0_5 = Version(notes=["Added record decorator that saves screenshots and makes videos."])
VERSION_0_0_4 = Version(notes=["MANIFEST.in is working; png files are included in the install."])
VERSION_0_0_3 = Version(notes=["Still trying to include .pngs..."])
VERSION_0_0_2 = Version(
    notes=[
        "Trying to get .png files to be included in the install, "
        "because this will allow the sample fonts to work out of the box."
    ]
)
VERSION_0_0_1 = Version(notes=["Initial version."])
