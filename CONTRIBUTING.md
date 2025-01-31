# แนวทางการมีส่วนร่วมในการพัฒนา

ขอบคุณที่สนใจมีส่วนร่วมในการพัฒนา MediTech HealthCheckup! 🎉

## 📝 วิธีการมีส่วนร่วม

### 1. การรายงานปัญหา (Issues)

- ตรวจสอบว่าปัญหาที่พบยังไม่มีการรายงานในส่วน Issues
- ใช้ template ที่เตรียมไว้ในการรายงานปัญหา
- ให้รายละเอียดที่ชัดเจนและขั้นตอนการทำซ้ำปัญหา
- แนบ screenshots หรือ logs ที่เกี่ยวข้อง

### 2. การส่ง Pull Request

1. Fork repository นี้
2. สร้าง branch ใหม่:
```bash
git checkout -b feature/amazing-feature
# หรือ
git checkout -b bugfix/issue-123
```

3. ทำการแก้ไขโค้ดและ commit:
```bash
git add .
git commit -m "feat: add amazing feature"
# หรือ
git commit -m "fix: resolve issue #123"
```

4. Push ไปยัง branch ของคุณ:
```bash
git push origin feature/amazing-feature
```

5. สร้าง Pull Request ผ่าน GitHub

### 3. Commit Message Format

ใช้รูปแบบ Conventional Commits:

- `feat:` สำหรับ feature ใหม่
- `fix:` สำหรับการแก้ไขบัก
- `docs:` สำหรับการแก้ไขเอกสาร
- `style:` สำหรับการจัดรูปแบบโค้ด
- `refactor:` สำหรับการปรับปรุงโค้ด
- `test:` สำหรับการเพิ่ม/แก้ไข tests
- `chore:` สำหรับการเปลี่ยนแปลงอื่นๆ

ตัวอย่าง:
```
feat: เพิ่มระบบการค้นหาผู้ป่วย
fix: แก้ไขปัญหาการแสดงผลรายงาน
docs: อัปเดตคู่มือการติดตั้ง
```

## 🧪 การทดสอบ

- รัน tests ก่อน commit:
```bash
pytest
```

- ตรวจสอบ code style:
```bash
black .
flake8
mypy .
```

## 📋 Checklist ก่อนส่ง PR

- [ ] รันและผ่าน tests ทั้งหมด
- [ ] โค้ดผ่านการตรวจสอบด้วย linter
- [ ] เพิ่ม/อัปเดตเอกสารที่เกี่ยวข้อง
- [ ] commit messages ถูกต้องตามรูปแบบ
- [ ] อธิบายการเปลี่ยนแปลงใน PR อย่างชัดเจน

## 🎨 Code Style

### Python
- ใช้ Black formatter
- ปฏิบัติตาม PEP 8
- ใช้ Type hints
- เขียน docstrings ในรูปแบบ Google style

### SQL
- ใช้ตัวพิมพ์ใหญ่สำหรับ keywords
- ใช้ snake_case สำหรับชื่อตาราง/คอลัมน์
- เพิ่ม comments อธิบายการทำงานที่ซับซ้อน

## 📚 เอกสาร

- อัปเดตเอกสารที่เกี่ยวข้องเมื่อมีการเปลี่ยนแปลง
- เพิ่มตัวอย่างการใช้งานสำหรับ features ใหม่
- ตรวจสอบความถูกต้องของลิงก์และรูปภาพ

## 🤝 Code Review

- ตอบกลับ reviews อย่างสร้างสรรค์
- อธิบายเหตุผลของการเปลี่ยนแปลง
- แก้ไขตาม feedback ที่ได้รับ

## 🔒 Security

- ไม่ commit sensitive data
- รายงานช่องโหว่ด้านความปลอดภัยทันที
- ใช้ environment variables สำหรับค่า configuration

## 📞 การติดต่อ

- GitHub Issues สำหรับรายงานปัญหา
- Discussions สำหรับคำถามและการพูดคุย
- Email: dev@meditech.com สำหรับเรื่องอื่นๆ

## 📜 License

การมีส่วนร่วมทั้งหมดอยู่ภายใต้ MIT License 