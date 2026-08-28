from sqlalchemy.orm import Session
from models import Setting

class OwnerControlCenter:
    @staticmethod
    def get_setting(db: Session, key: str, default: str = "") -> str:
        setting = db.query(Setting).filter(Setting.key == key).first()
        return setting.value if setting else default

    @staticmethod
    def update_setting(db: Session, key: str, value: str):
        setting = db.query(Setting).filter(Setting.key == key).first()
        if not setting:
            setting = Setting(key=key, value=str(value))
            db.add(setting)
        else:
            setting.value = str(value)
        db.commit()
