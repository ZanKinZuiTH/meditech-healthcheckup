"""
AI Diagnosis Service - ระบบวินิจฉัยโรคเบื้องต้นด้วย AI

คำอธิบายสำหรับนักศึกษา:
1. ระบบนี้ใช้ Medical QA Model จาก Hugging Face ในการวินิจฉัยโรคเบื้องต้น
2. โมเดลที่ใช้คือ BioBERT ที่ train ด้วยข้อมูลทางการแพทย์
3. มีระบบตรวจจับสัญญาณอันตรายและให้คำแนะนำเบื้องต้น

การทำงานหลัก:
1. รับข้อมูลอาการและรายละเอียดผู้ป่วย
2. ประมวลผลด้วย AI Model
3. วิเคราะห์ความเสี่ยงและสัญญาณอันตราย
4. ให้ผลการวินิจฉัยและคำแนะนำ

ข้อควรระวัง:
- ผลการวินิจฉัยเป็นเพียงการคัดกรองเบื้องต้น
- ควรปรึกษาแพทย์เสมอสำหรับการวินิจฉัยที่แม่นยำ
- กรณีพบสัญญาณอันตราย ให้รีบพบแพทย์ทันที
"""

from typing import Dict, List, Optional
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from ..core.config import settings
from ..schemas.diagnosis import DiagnosisInput, DiagnosisResult

logger = logging.getLogger(__name__)

class AIDiagnosisService:
    """บริการวินิจฉัยโรคเบื้องต้นด้วย AI
    
    คำอธิบายสำหรับนักศึกษา:
    - __init__: เตรียมตัวแปรและค่าเริ่มต้น
    - initialize: โหลดโมเดลและตั้งค่าระบบ
    - get_diagnosis: ฟังก์ชันหลักในการวินิจฉัย
    """
    
    def __init__(self):
        """เตรียมตัวแปรเริ่มต้น
        
        model_name: ชื่อโมเดล BioBERT จาก Hugging Face
        tokenizer: ใช้แปลงข้อความเป็น tokens
        model: โมเดล AI สำหรับวินิจฉัย
        qa_pipeline: pipeline สำหรับถาม-ตอบ
        initialized: สถานะการโหลดโมเดล
        """
        self.model_name = "GanjinZero/biobert_v1.1_pubmed_squad"
        self.tokenizer = None
        self.model = None
        self.qa_pipeline = None
        self.initialized = False
        
    async def initialize(self):
        """โหลดโมเดลและตั้งค่าเริ่มต้น
        
        ขั้นตอน:
        1. โหลด tokenizer สำหรับแปลงข้อความ
        2. โหลดโมเดล AI พร้อมการตั้งค่า
        3. สร้าง pipeline สำหรับถาม-ตอบ
        """
        if not self.initialized:
            try:
                logger.info(f"กำลังโหลดโมเดล {self.model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForQuestionAnswering.from_pretrained(
                    self.model_name,
                    device_map="auto",  # ใช้ GPU ถ้ามี
                    load_in_8bit=True   # ประหยัด memory
                )
                self.qa_pipeline = pipeline(
                    "question-answering",
                    model=self.model,
                    tokenizer=self.tokenizer
                )
                self.initialized = True
                logger.info("โหลดโมเดลสำเร็จ")
            except Exception as e:
                logger.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {str(e)}")
                raise
    
    async def get_diagnosis(self, input_data: DiagnosisInput) -> DiagnosisResult:
        """วินิจฉัยโรคเบื้องต้นจากอาการ
        
        ขั้นตอน:
        1. ตรวจสอบการโหลดโมเดล
        2. สร้างคำถามจากอาการ
        3. ดึงข้อมูลทางการแพทย์ที่เกี่ยวข้อง
        4. วิเคราะห์ด้วยโมเดล AI
        5. แปลงผลลัพธ์เป็นรูปแบบที่ใช้งาน
        
        Args:
            input_data: ข้อมูลอาการและรายละเอียดผู้ป่วย
            
        Returns:
            DiagnosisResult: ผลการวินิจฉัยเบื้องต้น
        """
        if not self.initialized:
            await self.initialize()
            
        try:
            # สร้างคำถามจากอาการ
            symptoms_text = ", ".join(input_data.symptoms)
            question = f"What are the possible conditions for these symptoms: {symptoms_text}?"
            
            # ใช้ context จากฐานความรู้ทางการแพทย์
            context = self._get_medical_context(input_data.symptoms)
            
            # ใช้โมเดลวิเคราะห์
            result = self.qa_pipeline(
                question=question,
                context=context,
                max_answer_length=100
            )
            
            # แปลงผลลัพธ์เป็น DiagnosisResult
            return DiagnosisResult(
                possible_conditions=self._parse_conditions(result["answer"]),
                confidence_score=result["score"],
                recommendation=self._generate_recommendation(result["answer"]),
                warning_signs=self._check_warning_signs(input_data.symptoms)
            )
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการวินิจฉัย: {str(e)}")
            raise
    
    def _get_medical_context(self, symptoms: List[str]) -> str:
        """ดึงข้อมูลทางการแพทย์ที่เกี่ยวข้องกับอาการ
        
        คำอธิบายสำหรับนักศึกษา:
        - ในอนาคตควรเชื่อมต่อกับฐานข้อมูลความรู้ทางการแพทย์
        - ปัจจุบันใช้ข้อมูลตัวอย่างเพื่อการสาธิต
        """
        return """
        Common symptoms and their related conditions:
        Fever can be caused by infections, inflammations, or other medical conditions.
        Headache might indicate stress, migraine, tension, or more serious conditions.
        Fatigue could be due to lack of sleep, anemia, or underlying health issues.
        Nausea might be related to digestive issues, pregnancy, or other conditions.
        Chest pain could indicate heart problems, anxiety, or muscle strain.
        Shortness of breath might be related to respiratory or cardiac issues.
        Dizziness can be caused by inner ear problems, low blood pressure, or anxiety.
        Joint pain could be due to arthritis, injury, or inflammatory conditions.
        """
    
    def _parse_conditions(self, answer: str) -> List[str]:
        """แยกวิเคราะห์โรคที่เป็นไปได้จากคำตอบ
        
        คำอธิบายสำหรับนักศึกษา:
        - แยกคำตอบเป็นรายการโรคที่เป็นไปได้
        - จำกัดจำนวนโรคที่แสดงเพื่อไม่ให้มากเกินไป
        """
        conditions = [c.strip() for c in answer.split(",")]
        return conditions[:5]  # จำกัดจำนวนโรคที่เป็นไปได้
    
    def _generate_recommendation(self, diagnosis: str) -> str:
        """สร้างคำแนะนำเบื้องต้นจากการวินิจฉัย
        
        คำอธิบายสำหรับนักศึกษา:
        - ควรพัฒนาให้คำแนะนำที่เฉพาะเจาะจงตามผลวินิจฉัย
        - เพิ่มการอ้างอิงแหล่งข้อมูลทางการแพทย์
        """
        return """
        คำแนะนำเบื้องต้น:
        1. ควรพบแพทย์เพื่อตรวจวินิจฉัยอย่างละเอียด
        2. สังเกตอาการและจดบันทึกการเปลี่ยนแปลง
        3. หากมีอาการรุนแรงขึ้นให้รีบไปพบแพทย์ทันที
        4. พักผ่อนให้เพียงพอและดื่มน้ำมากๆ
        5. หลีกเลี่ยงการออกกำลังกายหนักระหว่างมีอาการ
        """
    
    def _check_warning_signs(self, symptoms: List[str]) -> List[str]:
        """ตรวจสอบสัญญาณอันตราย
        
        คำอธิบายสำหรับนักศึกษา:
        - ตรวจสอบอาการที่อาจเป็นอันตราย
        - แจ้งเตือนให้รีบพบแพทย์ทันทีถ้าพบ
        """
        warning_signs = []
        dangerous_symptoms = {
            "เจ็บหน้าอกรุนแรง",
            "หายใจลำบาก",
            "ชัก",
            "หมดสติ",
            "ไข้สูงมาก",
            "เลือดออกรุนแรง",
            "ปวดท้องรุนแรง",
            "อาเจียนเป็นเลือด"
        }
        
        for symptom in symptoms:
            if symptom.lower() in [s.lower() for s in dangerous_symptoms]:
                warning_signs.append(
                    f"อาการ '{symptom}' เป็นสัญญาณอันตราย ควรไปพบแพทย์ทันที"
                )
        
        return warning_signs 