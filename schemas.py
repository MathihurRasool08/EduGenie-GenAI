from pydantic import BaseModel, Field, field_validator

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input text cannot be empty.")
        return value

class QARequest(TextRequest):
    question: str | None = None

    @field_validator("question")
    @classmethod
    def strip_question(cls, value: str | None) -> str | None:
        return value.strip() if value else value

class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str

class QuizResponse(BaseModel):
    title: str
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)

class LearningStep(BaseModel):
    level: str
    topic: str
    why_it_matters: str
    estimated_time: str
    resources: list[str] = Field(default_factory=list)

class LearningPathResponse(BaseModel):
    topic: str
    learner_level: str
    goal: str
    steps: list[LearningStep]
    study_tips: list[str]
