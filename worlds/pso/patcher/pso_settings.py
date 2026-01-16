import settings

class PSOIsoFile(settings.UserFilePath):
    """
    Locate the user's Phantasy Star Online Episode 1 and 2 Plus ISO file.
    """

    description = "Phantasy Star Online Episode 1 & 2 Plus ISO"
    copy_to = None


class PSOSettings(settings.Group):
    iso_file: PSOIsoFile = PSOIsoFile(PSOIsoFile.copy_to)