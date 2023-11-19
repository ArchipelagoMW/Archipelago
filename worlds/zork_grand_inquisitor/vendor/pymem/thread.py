import ctypes

import pymem.memory
import pymem.ressources.kernel32
import pymem.ressources.ntdll
import pymem.ressources.structure


class Thread(object):
    """
    Provides basic thread information such as TEB.

    Parameters
    ----------
    process_handle: int
        A handle to an opened process
    th_entry_32: ThreadEntry32
        Target thread's entry object
    """

    def __init__(self, process_handle, th_entry_32):
        self.process_handle = process_handle
        self.thread_id = th_entry_32.th32ThreadID
        self.th_entry_32 = th_entry_32
        self.teb_address = None
        # teb should be tested, not working on x64
        # self.teb = self._query_teb()

    def _query_teb(self):
        """Query current thread information to extract the TEB structure.

            :return: TEB information
            :rtype: pymem.ressources.structure.SMALL_TEB
        """
        THREAD_QUERY_INFORMATION = 0x0040

        thread_handle = pymem.ressources.kernel32.OpenThread(
            THREAD_QUERY_INFORMATION, False, self.th_entry_32.th32ThreadID
        )
        res = pymem.ressources.structure.THREAD_BASIC_INFORMATION()
        ThreadBasicInformation = 0x0

        pymem.ressources.ntdll.NtQueryInformationThread(
            thread_handle,
            ThreadBasicInformation,
            ctypes.byref(res),
            ctypes.sizeof(res),
            None
        )
        self.teb_address = res.TebBaseAddress
        data = pymem.memory.read_bytes(
            self.process_handle,
            res.TebBaseAddress,
            ctypes.sizeof(pymem.ressources.structure.SMALL_TEB)
        )
        teb = pymem.ressources.structure.SMALL_TEB.from_buffer_copy(data)
        pymem.ressources.kernel32.CloseHandle(thread_handle)
        return teb
