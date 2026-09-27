"""模擬的「硬體」:一顆只會讀寫固定大小區塊的磁碟。這個檔案已經寫好,不要改。

它刻意很難用:只能一次讀寫一整個區塊,而且區塊大小每顆 disk 可能不同。
任務 3 要你在它上面蓋一層抽象(KVStore),讓使用者完全不用知道區塊的存在。
"""


class RawDisk:
    def __init__(self, n_blocks=256, block_size=64):
        if n_blocks <= 0 or block_size <= 0:
            raise ValueError("n_blocks 與 block_size 都要是正整數")
        self.n_blocks = n_blocks
        self.block_size = block_size
        self._blocks = [bytes(block_size) for _ in range(n_blocks)]
        self.reads = 0      # 讀了幾次區塊(可以拿來量測抽象層的成本)
        self.writes = 0

    def read_block(self, i):
        """回傳第 i 個區塊的內容(剛好 block_size 個位元組)。"""
        if not 0 <= i < self.n_blocks:
            raise IndexError(f"block {i} 不存在(共 {self.n_blocks} 個)")
        self.reads += 1
        return self._blocks[i]

    def write_block(self, i, data):
        """把 data 寫進第 i 個區塊。data 必須剛好 block_size 個位元組。"""
        if not 0 <= i < self.n_blocks:
            raise IndexError(f"block {i} 不存在(共 {self.n_blocks} 個)")
        if not isinstance(data, (bytes, bytearray)) or len(data) != self.block_size:
            raise ValueError(f"每次必須寫入剛好 {self.block_size} 個位元組")
        self.writes += 1
        self._blocks[i] = bytes(data)
