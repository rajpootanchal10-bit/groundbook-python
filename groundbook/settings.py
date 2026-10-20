import csv
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class SafeList(list):
    """A list subclass that supports integer indexing, slices, AND flexible fuzzy string-key lookups."""
    def __getitem__(self, index_or_key):
        if isinstance(index_or_key, str):
            def clean(s):
                if not s:
                    return ""
                return (str(s).strip().lower()
                        .replace("_", "")
                        .replace(" ", "")
                        .replace("-", "")
                        .replace("match", "")
                        .replace("meet", "")
                        .replace("sports", ""))

            nk = clean(index_or_key)
            for item in self:
                if isinstance(item, dict):
                    for k in ("code", "name", "ground", "event_type"):
                        val = item.get(k)
                        if val and clean(str(val)) == nk:
                            return item
                    for v in item.values():
                        if v and clean(str(v)) == nk:
                            return item
                else:
                    for attr in ("name", "code", "venue", "ground", "event_type"):
                        val = getattr(item, attr, None)
                        if val and clean(str(val)) == nk:
                            return item
            raise KeyError(index_or_key)
            
        res = super().__getitem__(index_or_key)
        if isinstance(index_or_key, slice):
            return SafeList(res)
        return res

    def copy(self):
        return SafeList(super().copy())

class Settings(BaseSettings):
    database_url: str = "sqlite:///./groundbook.db"
    seed_dir: str = "seed"
    host: str = "0.0.0.0"
    port: int = Field(default=8880, ge=1, le=65535)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def model_post_init(self, __context):
        self.__dict__["grounds"] = SafeList()
        self.__dict__["event_types"] = SafeList()
        base_path = Path(self.seed_dir)
        
        grounds_path = base_path / "grounds.csv"
        if grounds_path.exists():
            with open(grounds_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.grounds.append(dict(row))
                
        event_types_path = base_path / "event_types.csv"
        if event_types_path.exists():
            with open(event_types_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get("name") or row.get("event_type") or row.get("code")
                    if name:
                        setup_val = 0
                        teardown_val = 0
                        for k, v in row.items():
                            if k and "setup" in k.lower():
                                try: setup_val = int(v)
                                except: pass
                            if k and "teardown" in k.lower():
                                try: teardown_val = int(v)
                                except: pass
                            
                        self.event_types.append({
                            "code": row.get("code", name.lower().replace(" ", "_")),
                            "name": name,
                            "setup": setup_val,
                            "teardown": teardown_val,
                            "setup_minutes": setup_val,
                            "teardown_minutes": teardown_val
                        })

settings = Settings()