from typing import Dict, List, Optional
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from ..core.config import settings
from ..schemas.diagnosis import DiagnosisInput, DiagnosisResult

logger = logging.getLogger(__name__)

class AIDiagnosisService:
    """บริการวินิจฉัยโรคเบื้องต้นด้วย AI"""
    
    def __init__(self):
        self.model_name = "GanjinZero/biobert_v1.1_pubmed_squad"
        self.tokenizer = None
        self.model = None
        self.qa_pipeline = None
        self.initialized = False
        
    async def initialize(self):
        """โหลดโมเดลและตั้งค่าเริ่มต้น"""
        if not self.initialized:
            try:
                logger.info(f"กำลังโหลดโมเดล {self.model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForQuestionAnswering.from_pretrained(
                    self.model_name,
                    device_map="auto",
                    load_in_8bit=True
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
        """วินิจฉัยโรคเบื้องต้นจากอาการ"""
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
        """ดึงข้อมูลทางการแพทย์ที่เกี่ยวข้องกับอาการ"""
        # TODO: เชื่อมต่อกับฐานข้อมูลความรู้ทางการแพทย์
        return """
        Common symptoms and their related conditions:
        Fever can be caused by infections, inflammations, or other medical conditions.
        Headache might indicate stress, migraine, tension, or more serious conditions.
        Fatigue could be due to lack of sleep, anemia, or underlying health issues.
        Nausea might be related to digestive issues, pregnancy, or other conditions.
        """
    
    def _parse_conditions(self, answer: str) -> List[str]:
        """แยกวิเคราะห์โรคที่เป็นไปได้จากคำตอบ"""
        # TODO: ปรับปรุงการแยกวิเคราะห์ให้แม่นยำขึ้น
        conditions = [c.strip() for c in answer.split(",")]
        return conditions[:5]  # จำกัดจำนวนโรคที่เป็นไปได้
    
    def _generate_recommendation(self, diagnosis: str) -> str:
        """สร้างคำแนะนำเบื้องต้นจากการวินิจฉัย"""
        # TODO: พัฒนาระบบให้คำแนะนำที่เฉพาะเจาะจง
        return """
        คำแนะนำเบื้องต้น:
        1. ควรพบแพทย์เพื่อตรวจวินิจฉัยอย่างละเอียด
        2. สังเกตอาการและจดบันทึกการเปลี่ยนแปลง
        3. หากมีอาการรุนแรงขึ้นให้รีบไปพบแพทย์ทันที
        """
    
    def _check_warning_signs(self, symptoms: List[str]) -> List[str]:
        """ตรวจสอบสัญญาณอันตราย"""
        warning_signs = []
        dangerous_symptoms = {
            "เจ็บหน้าอกรุนแรง",
            "หายใจลำบาก",
            "ชัก",
            "หมดสติ"
        }
        
        for symptom in symptoms:
            if symptom in dangerous_symptoms:
                warning_signs.append(
                    f"อาการ '{symptom}' เป็นสัญญาณอันตราย ควรไปพบแพทย์ทันที"
                )
        
        return warning_signs 