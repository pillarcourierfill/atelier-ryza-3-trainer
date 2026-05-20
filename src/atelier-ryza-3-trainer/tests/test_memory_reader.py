import unittest
from unittest.mock import patch, MagicMock
from src.memory_reader import MemoryReader

class TestMemoryReader(unittest.TestCase):
    """Unit tests for MemoryReader class."""

    @patch('src.memory_reader.psutil.process_iter')
    def test_open_process_success(self, mock_process_iter):
        """Test successful process attachment."""
        mock_proc = MagicMock()
        mock_proc.info = {'pid': 1234, 'name': 'AtelierRyza3.exe'}
        mock_process_iter.return_value = [mock_proc]

        reader = MemoryReader('AtelierRyza3.exe')
        with patch.object(reader.kernel32, 'OpenProcess', return_value=0xABC):
            result = reader.open_process()
            self.assertTrue(result)
            self.assertEqual(reader.pid, 1234)
            self.assertEqual(reader.process_handle, 0xABC)

    @patch('src.memory_reader.psutil.process_iter')
    def test_open_process_failure(self, mock_process_iter):
        """Test process attachment failure."""
        mock_process_iter.return_value = []
        reader = MemoryReader('AtelierRyza3.exe')
        result = reader.open_process()
        self.assertFalse(result)
        self.assertIsNone(reader.pid)
        self.assertIsNone(reader.process_handle)

    def test_read_int_success(self):
        """Test reading an integer from memory."""
        reader = MemoryReader('AtelierRyza3.exe')
        reader.process_handle = 0xABC
        with patch.object(reader.kernel32, 'ReadProcessMemory', return_value=True) as mock_read:
            # Simulate buffer being set to 42
            def side_effect(handle, address, buffer, size, bytes_read):
                buffer.value = 42
                bytes_read.value = 4
                return True
            mock_read.side_effect = side_effect
            result = reader.read_int(0x1234)
            self.assertEqual(result, 42)

    def test_read_int_failure(self):
        """Test reading memory when it fails."""
        reader = MemoryReader('AtelierRyza3.exe')
        reader.process_handle = 0xABC
        with patch.object(reader.kernel32, 'ReadProcessMemory', return_value=False):
            with self.assertRaises(RuntimeError):
                reader.read_int(0x1234)

    def test_write_int_success(self):
        """Test writing an integer to memory."""
        reader = MemoryReader('AtelierRyza3.exe')
        reader.process_handle = 0xABC
        with patch.object(reader.kernel32, 'WriteProcessMemory', return_value=True) as mock_write:
            reader.write_int(0x1234, 99)
            mock_write.assert_called_once()

    def test_write_int_failure(self):
        """Test writing memory when it fails."""
        reader = MemoryReader('AtelierRyza3.exe')
        reader.process_handle = 0xABC
        with patch.object(reader.kernel32, 'WriteProcessMemory', return_value=False):
            with self.assertRaises(RuntimeError):
                reader.write_int(0x1234, 99)

    def test_close(self):
        """Test closing the process handle."""
        reader = MemoryReader('AtelierRyza3.exe')
        reader.process_handle = 0xABC
        with patch.object(reader.kernel32, 'CloseHandle') as mock_close:
            reader.close()
            mock_close.assert_called_once_with(0xABC)
            self.assertIsNone(reader.process_handle)

if __name__ == '__main__':
    unittest.main()
