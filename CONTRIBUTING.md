# Contributing to MediTech HealthCheckup System

ขอบคุณที่สนใจมีส่วนร่วมในการพัฒนา MediTech HealthCheckup System! เราต้องการให้การมีส่วนร่วมในโปรเจคนี้เป็นประสบการณ์ที่ดีสำหรับทุกคน

## วิธีการมีส่วนร่วม

1. **Fork Repository**
   - Fork repository นี้ไปยังบัญชี GitHub ของคุณ
   - Clone repository ที่ fork ไปยังเครื่องของคุณ

2. **สร้าง Branch**
   - สร้าง branch ใหม่สำหรับฟีเจอร์หรือการแก้ไขของคุณ
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **พัฒนาและทดสอบ**
   - เขียนโค้ดตามมาตรฐานของโปรเจค
   - เพิ่ม unit tests สำหรับฟีเจอร์ใหม่
   - รัน tests ให้ผ่านทั้งหมด
   ```bash
   pytest
   ```

4. **Commit Changes**
   - ใช้ commit message ที่ชัดเจนและเข้าใจง่าย
   ```bash
   git commit -m "Add feature: your feature description"
   ```

5. **Push และสร้าง Pull Request**
   - Push การเปลี่ยนแปลงไปยัง fork repository ของคุณ
   ```bash
   git push origin feature/your-feature-name
   ```
   - สร้าง Pull Request ไปยัง main branch ของโปรเจค

## มาตรฐานการเขียนโค้ด

1. **Python Style Guide**
   - ปฏิบัติตาม PEP 8
   - ใช้ Type Hints
   - เขียน docstrings สำหรับฟังก์ชันและคลาส

2. **การตั้งชื่อ**
   - ใช้ snake_case สำหรับฟังก์ชันและตัวแปร
   - ใช้ PascalCase สำหรับคลาส
   - ใช้ UPPERCASE สำหรับค่าคงที่

3. **การจัดรูปแบบโค้ด**
   - ใช้ Black formatter
   - ใช้ isort สำหรับจัดเรียง imports
   - ใช้ Flake8 linter

## การรายงานปัญหา

1. **Bug Reports**
   - ใช้ GitHub Issues
   - อธิบายปัญหาให้ชัดเจน
   - ระบุขั้นตอนการทำซ้ำ
   - แนบ error messages หรือ screenshots

2. **Feature Requests**
   - อธิบายฟีเจอร์ที่ต้องการ
   - ระบุเหตุผลและประโยชน์
   - เสนอแนวทางการพัฒนา (ถ้ามี)

## แนวทางการพัฒนา

1. **Backend Development**
   - ใช้ FastAPI framework
   - เขียน API documentation
   - ทำ input validation
   - จัดการ error handling

2. **Frontend Development**
   - ใช้ PyQt6
   - ทำตาม UI/UX guidelines
   - รองรับ responsive design
   - เพิ่ม accessibility features

3. **Database**
   - ใช้ SQLAlchemy ORM
   - เขียน database migrations
   - optimize queries
   - จัดการ data integrity

4. **Testing**
   - Unit tests ครอบคลุม
   - Integration tests
   - Performance tests
   - Security tests

## Security Guidelines

1. **Authentication & Authorization**
   - ใช้ JWT tokens
   - จัดการ user roles
   - ป้องกัน SQL injection
   - ป้องกัน XSS attacks

2. **Data Protection**
   - เข้ารหัสข้อมูลสำคัญ
   - ใช้ HTTPS
   - จัดการ session security
   - ทำ input sanitization

## Documentation

1. **Code Documentation**
   - เขียน docstrings
   - อธิบาย complex logic
   - update API documentation
   - เพิ่ม code examples

2. **User Documentation**
   - คู่มือการติดตั้ง
   - คู่มือการใช้งาน
   - troubleshooting guide
   - FAQs

## Community

- เคารพผู้อื่น
- ให้ feedback ที่สร้างสรรค์
- ช่วยเหลือผู้เริ่มต้น
- แบ่งปันความรู้

## License

โปรเจคนี้เผยแพร่ภายใต้ MIT License - ดูรายละเอียดได้ที่ [LICENSE](LICENSE) 