import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import json
import os

logger = logging.getLogger(__name__)

class CacheItem:
    def __init__(self, value: Any, expires_in: int = 300):
        self.value = value
        self.timestamp = datetime.now()
        self.expires_in = expires_in
    
    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.timestamp + timedelta(seconds=self.expires_in)

class Cache:
    def __init__(self):
        self._cache: Dict[str, CacheItem] = {}
        self._disk_cache_dir = "cache"
        
        # สร้างโฟลเดอร์สำหรับ disk cache
        if not os.path.exists(self._disk_cache_dir):
            os.makedirs(self._disk_cache_dir)
    
    def get(self, key: str) -> Optional[Any]:
        """ดึงข้อมูลจาก cache"""
        if key in self._cache:
            item = self._cache[key]
            if not item.is_expired:
                logger.debug(f"Cache hit: {key}")
                return item.value
            else:
                logger.debug(f"Cache expired: {key}")
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, expires_in: int = 300):
        """เก็บข้อมูลใน cache"""
        self._cache[key] = CacheItem(value, expires_in)
        logger.debug(f"Cache set: {key}")
    
    def delete(self, key: str):
        """ลบข้อมูลจาก cache"""
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted: {key}")
    
    def clear(self):
        """ล้าง cache ทั้งหมด"""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def save_to_disk(self, key: str, value: Any):
        """บันทึก cache ลงดิสก์"""
        try:
            file_path = os.path.join(self._disk_cache_dir, f"{key}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(value, f)
            logger.debug(f"Cache saved to disk: {key}")
        except Exception as e:
            logger.error(f"Failed to save cache to disk: {str(e)}")
    
    def load_from_disk(self, key: str) -> Optional[Any]:
        """โหลด cache จากดิสก์"""
        try:
            file_path = os.path.join(self._disk_cache_dir, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    value = json.load(f)
                logger.debug(f"Cache loaded from disk: {key}")
                return value
        except Exception as e:
            logger.error(f"Failed to load cache from disk: {str(e)}")
        return None
    
    async def preload_common_data(self, api_client):
        """โหลดข้อมูลที่ใช้บ่อยเข้า cache"""
        try:
            # โหลดข้อมูลพื้นฐาน
            themes = await api_client.get_themes()
            self.set("themes", themes, expires_in=3600)
            
            # โหลดการตั้งค่าผู้ใช้
            settings = await api_client.get_user_settings()
            self.set("user_settings", settings, expires_in=3600)
            
            # บันทึกลงดิสก์
            self.save_to_disk("themes", themes)
            self.save_to_disk("user_settings", settings)
            
            logger.info("Common data preloaded successfully")
        except Exception as e:
            logger.error(f"Failed to preload common data: {str(e)}")
    
    def get_cached_or_fetch(self, key: str, fetch_func, expires_in: int = 300):
        """ดึงข้อมูลจาก cache หรือเรียก API ถ้าไม่มี"""
        value = self.get(key)
        if value is None:
            value = fetch_func()
            self.set(key, value, expires_in)
        return value 