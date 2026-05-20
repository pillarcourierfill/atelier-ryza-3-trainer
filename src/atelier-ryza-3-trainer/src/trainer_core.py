from src.memory_reader import MemoryReader

class AtelierRyza3Trainer:
    """
    Core trainer class for Atelier Ryza 3: Alchemist of the End & the Secret Key.
    Provides cheats for infinite HP, MP, AP, and item quantity.
    """

    # Example memory offsets (static for demonstration; in real usage, these would be
    # dynamically resolved via signature scanning or pointer chains)
    HP_OFFSET = 0x00A1B2C0
    MP_OFFSET = 0x00A1B2C4
    AP_OFFSET = 0x00A1B2C8
    ITEM_QUANTITY_OFFSET = 0x00A1B2D0

    def __init__(self):
        self.reader = MemoryReader("AtelierRyza3.exe")
        self.attached = False

    def attach(self) -> bool:
        """Attach to the game process."""
        self.attached = self.reader.open_process()
        return self.attached

    def detach(self) -> None:
        """Detach from the game process."""
        self.reader.close()
        self.attached = False

    def set_infinite_hp(self, enable: bool) -> None:
        """Set HP to maximum when enabled."""
        if not self.attached:
            raise RuntimeError("Not attached to process")
        if enable:
            # Write a large value (e.g., 9999) to the HP address
            self.reader.write_int(self.HP_OFFSET, 9999)
        # In a real trainer, you would toggle a freeze loop

    def set_infinite_mp(self, enable: bool) -> None:
        """Set MP to maximum when enabled."""
        if not self.attached:
            raise RuntimeError("Not attached to process")
        if enable:
            self.reader.write_int(self.MP_OFFSET, 9999)

    def set_infinite_ap(self, enable: bool) -> None:
        """Set AP to maximum when enabled."""
        if not self.attached:
            raise RuntimeError("Not attached to process")
        if enable:
            self.reader.write_int(self.AP_OFFSET, 9999)

    def set_infinite_items(self, enable: bool) -> None:
        """Set item quantity to maximum when enabled."""
        if not self.attached:
            raise RuntimeError("Not attached to process")
        if enable:
            self.reader.write_int(self.ITEM_QUANTITY_OFFSET, 99)
