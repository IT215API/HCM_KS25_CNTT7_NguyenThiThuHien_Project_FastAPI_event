from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.user_model import UserModel
from app.models.event_model import EventModel
from app.models.event_task import EventTaskModel
from app.models.event_staff import EventStaffModel
from app.core.security import hash_password


def seed_data():
    db = SessionLocal()
    try:
        print("Đang tiến hành seed dữ liệu...")

        admin = db.query(UserModel).filter(
            UserModel.email == "admin@gmail.com").first()
        if not admin:
            admin = UserModel(
                email="admin@gmail.com",
                password_hash=hash_password("123456"),
                full_name="Quản Trị Viên",
                role="Admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Đã tạo tài khoản Admin: admin@gmail.com / 123456")
        else:
            print("Tài khoản Admin đã tồn tại.")

        user_staff = db.query(UserModel).filter(
            UserModel.email == "user@gmail.com").first()
        if not user_staff:
            user_staff = UserModel(
                email="user@gmail.com",
                password_hash=hash_password("123456"),
                full_name="Nguyễn Văn A",
                role="User",
                is_active=True
            )
            db.add(user_staff)
            db.commit()
            db.refresh(user_staff)
            print("Đã tạo tài khoản User: user@gmail.com / 123456")
        else:
            print("Tài khoản User đã tồn tại.")

        event = db.query(EventModel).first()
        if not event:
            event = EventModel(
                name="Hội Thảo Công Nghệ TechTalk 2026",
                description="Hội thảo chuyên sâu về kiến trúc FastAPI, Microservices và Hệ thống bảo mật.",
                owner_id=admin.id
            )

            db.add(event)
            db.commit()
            db.refresh(event)
            print("Đã tạo sự kiện mẫu thành công.")

            staff_owner = EventStaffModel(
                event_id=event.id,
                user_id=admin.id,
                role="OWNER"
            )
            staff_member = EventStaffModel(
                event_id=event.id,
                user_id=user_staff.id,
                role="MEMBER"
            )
            db.add_all([staff_owner, staff_member])
            db.commit()
            print("Phân quyền thành công Ban tổ chức (1 OWNER, 1 MEMBER)")

            task1 = EventTaskModel(
                event_id=event.id,
                title="Chuẩn bị hội trường & Âm thanh",
                description="Lắp đặt mic, loa và máy chiếu.",
                assignee_id=user_staff.id,
                status="TODO",
                priority="HIGH",
                due_date=datetime.now() + timedelta(days=2)
            )
            db.add(task1)
            db.commit()
            print("Đã tạo công việc mẫu.")

        else:
            print("Dữ liệu sự kiện đã tồn tại, bỏ qua bước seed sự kiện.")

        print("Hoàn tất Seed dữ liệu thử nghiệm!")

    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed dữ liệu: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
