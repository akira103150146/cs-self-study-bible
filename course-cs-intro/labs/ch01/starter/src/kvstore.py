"""任務 3:在 RawDisk(只會讀寫固定大小區塊的「硬體」)上面蓋一層抽象。

使用者只看得到 put / get / delete / keys,完全不需要知道區塊的存在。
要求:
- 資料必須真的存在 disk 上:用同一顆 disk 再開一個 KVStore,要讀得到之前存的東西。
- 不能假設區塊大小:同一段使用者程式,換一顆 block_size 不同的 disk 也要能跑。
- 值(value)是 bytes,可能比一個區塊大很多。
"""
from rawdisk import RawDisk  # noqa: F401  (型別提示用)


class KVStore:
    def __init__(self, disk):
        self.disk = disk
        # TODO

    def put(self, key: str, value: bytes) -> None:
        raise NotImplementedError

    def get(self, key: str) -> bytes:
        """key 不存在時丟 KeyError。"""
        raise NotImplementedError

    def delete(self, key: str) -> None:
        """key 不存在時丟 KeyError。"""
        raise NotImplementedError

    def keys(self) -> list:
        raise NotImplementedError
