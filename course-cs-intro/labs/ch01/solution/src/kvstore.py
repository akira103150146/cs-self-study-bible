"""任務 3 參考解:在 RawDisk 上蓋一個 key-value store。

做法(刻意選最單純、正確的):整個字典序列化成一串位元組,前 8 個位元組放長度,
從區塊 0 開始依序寫滿需要的區塊。讀的時候反過來。每次修改都整份重寫——慢,但正確;
「怎麼只改動需要的區塊」留給延伸專案。
"""
import json

from rawdisk import RawDisk  # noqa: F401

HEADER = 8


class KVStore:
    def __init__(self, disk):
        self.disk = disk
        self._data = self._load()

    # ---- 對外的介面:使用者只看得到這四個方法 ----
    def put(self, key: str, value: bytes) -> None:
        self._data[key] = bytes(value)
        self._save()

    def get(self, key: str) -> bytes:
        return self._data[key]

    def delete(self, key: str) -> None:
        del self._data[key]
        self._save()

    def keys(self) -> list:
        return list(self._data)

    # ---- 以下是被藏起來的細節:區塊怎麼切、怎麼存 ----
    def _load(self):
        first = b""
        i = 0
        while len(first) < HEADER:
            first += self.disk.read_block(i)
            i += 1
        n = int.from_bytes(first[:HEADER], "little")
        if n == 0:
            return {}
        need = HEADER + n
        raw = first
        while len(raw) < need:
            raw += self.disk.read_block(i)
            i += 1
        obj = json.loads(raw[HEADER:need].decode("utf-8"))
        return {k: bytes.fromhex(v) for k, v in obj.items()}

    def _save(self):
        payload = json.dumps({k: v.hex() for k, v in self._data.items()}).encode("utf-8")
        blob = len(payload).to_bytes(HEADER, "little") + payload
        bs = self.disk.block_size
        n_blocks = -(-len(blob) // bs)
        if n_blocks > self.disk.n_blocks:
            raise ValueError("disk full")
        blob += bytes(n_blocks * bs - len(blob))
        for i in range(n_blocks):
            self.disk.write_block(i, blob[i * bs:(i + 1) * bs])
