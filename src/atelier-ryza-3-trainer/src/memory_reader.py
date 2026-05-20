import ctypes
import ctypes.wintypes

class MemoryReader:
    """
    Reads and writes process memory for Atelier Ryza 3.
    Uses Windows API via ctypes for external memory manipulation.
    """

    PROCESS_ALL_ACCESS = 0x1F0FFF
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    def __init__(self, process_name: str):
        self.process_name = process_name
        self.process_handle = None
        self.pid = None

    def open_process(self) -> bool:
        """Open the target process with full access rights."""
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.process_name:
                self.pid = proc.info['pid']
                self.process_handle = self.kernel32.OpenProcess(
                    self.PROCESS_ALL_ACCESS,
                    False,
                    self.pid
                )
                return self.process_handle is not None
        return False

    def read_int(self, address: int) -> int:
        """Read a 4-byte integer from the given memory address."""
        buffer = ctypes.c_int(0)
        bytes_read = ctypes.c_size_t(0)
        success = self.kernel32.ReadProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            ctypes.byref(buffer),
            ctypes.sizeof(buffer),
            ctypes.byref(bytes_read)
        )
        if not success:
            raise RuntimeError(f"Failed to read memory at {hex(address)}")
        return buffer.value

    def write_int(self, address: int, value: int) -> None:
        """Write a 4-byte integer to the given memory address."""
        buffer = ctypes.c_int(value)
        bytes_written = ctypes.c_size_t(0)
        success = self.kernel32.WriteProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            ctypes.byref(buffer),
            ctypes.sizeof(buffer),
            ctypes.byref(bytes_written)
        )
        if not success:
            raise RuntimeError(f"Failed to write memory at {hex(address)}")

    def close(self) -> None:
        """Close the process handle."""
        if self.process_handle:
            self.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
