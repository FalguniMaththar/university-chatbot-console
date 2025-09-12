from db_manager import init_db, list_faqs
import nlp_utils

class Chatbot:
    def __init__(self):
        init_db()
        self.refresh()
        self.intent_map = {
            'admission': "Admission details depend on the program. Visit admissions office or type 'admissions deadline'.",
            'timetable': "Check the student portal for class timetables.",
            'faculty': "Faculty contacts are available on the department page.",
            'fees': "Fee structure varies by program. Which program?",
            'result': "Results are posted on the university portal about 3–4 weeks after exams."
        }
        self.intent_keywords = {
            'admission': ['admission','apply','application','deadline','enroll'],
            'timetable': ['timetable','time table','schedule','class time'],
            'faculty': ['professor','faculty','teacher','lecturer','staff'],
            'fees': ['fee','fees','tuition','cost'],
            'result': ['result','grade','marks','score']
        }

    def refresh(self):
        self.faqs = list_faqs()

    def _detect_intent(self, text: str):
        t = text.lower()
        for intent, kws in self.intent_keywords.items():
            if any(kw in t for kw in kws):
                return intent
        return None

    def respond(self, text: str):
        if not text.strip():
            return "Please type a question or /help for commands."
        best, score = nlp_utils.best_match(text, self.faqs)
        if best:
            return best['answer']
        intent = self._detect_intent(text)
        if intent:
            return self.intent_map[intent]
        return "Sorry, I couldn't find an answer. Try /addfaq or /help."