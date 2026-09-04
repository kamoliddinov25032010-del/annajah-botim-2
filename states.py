from aiogram.fsm.state import State, StatesGroup

class AboutState(StatesGroup):
    waiting_photo = State()
    waiting_text = State()

class HikmatState(StatesGroup):
    waiting_photo = State()
    waiting_text = State()
    waiting_delete_number = State()

class TeacherState(StatesGroup):
    waiting_photo = State()
    waiting_name = State()
    waiting_subject = State()
    waiting_description = State()

    waiting_edit_number = State()
    waiting_new_photo = State()
    waiting_new_name = State()
    waiting_new_subject = State()
    waiting_new_description = State()

    waiting_delete_number = State()

class StaffState(StatesGroup):
    waiting_photo = State()
    waiting_name = State()
    waiting_position = State()
    waiting_description = State()

    waiting_edit_number = State()
    waiting_new_photo = State()
    waiting_new_name = State()
    waiting_new_position = State()
    waiting_new_description = State()

    waiting_delete_number = State()

class PdfState(StatesGroup):
    waiting_file = State()
    waiting_title = State()
    waiting_delete_number = State()
class CalligraphyState(StatesGroup):
    waiting_video = State()
    waiting_title = State()
    waiting_delete_number = State()
class CartoonState(StatesGroup):
    waiting_video = State()
    waiting_title = State()
    waiting_delete_number = State()
class StoryState(StatesGroup):
    waiting_video = State()
    waiting_title = State()
    waiting_delete_number = State()
class DictionaryState(StatesGroup):
    waiting_video = State()
    waiting_title = State()
    waiting_delete_number = State()
class AlphabetState(StatesGroup):
    waiting_video = State()
    waiting_title = State()
    waiting_delete_number = State()
class ContactState(StatesGroup):
    waiting_text = State()
    waiting_phone = State()
    waiting_delete = State()
class BroadcastState(StatesGroup):
    waiting_message = State()
class SearchState(StatesGroup):
    waiting_query = State()
    waiting_number = State()

    from aiogram.fsm.state import State, StatesGroup

class AIState(StatesGroup):
    chatting = State()
class AIState(StatesGroup):
    chatting = State()
    voice_question = State()
    testing = State()
    word_meaning = State()

class GifState(StatesGroup):
    waiting_gif = State()
    waiting_title = State()
    waiting_delete = State()

class GifState(StatesGroup):
    waiting_gif = State()
    waiting_title = State()
    waiting_delete = State()

class ParentState(StatesGroup):
    waiting_child_id = State()

class ParentLinkState(StatesGroup):
    waiting_parent_id = State()
    waiting_child_id = State()

class QAState(StatesGroup):
    waiting_question = State()
    waiting_answer = State()

class PrayerState(StatesGroup):
    waiting_city = State()

class RegistrationState(StatesGroup):
    waiting_fullname = State()
    waiting_age = State()
    waiting_phone = State()

class TeacherPanelState(StatesGroup):
    waiting_password = State()
    waiting_new_password = State()
    waiting_class_days = State()
    waiting_grade_value = State()
    waiting_grade_comment = State()

class TeacherAdminState(StatesGroup):
    waiting_teacher_pick = State()
    waiting_telegram_id = State()
    waiting_group_teacher_pick = State()
    waiting_group_name = State()
    waiting_group_delete_pick = State()

class RegistrationState(StatesGroup):
    waiting_student_name = State()
    waiting_student_phone = State()
    waiting_parent_name = State()
    waiting_parent_phone = State()

class AdminActionState(StatesGroup):
    waiting_ban_id = State()
    waiting_ban_reason = State()
    waiting_unban_id = State()
    waiting_dm_id = State()
    waiting_dm_text = State()

class HomeworkState(StatesGroup):
    waiting_content = State()

class FeedbackState(StatesGroup):
    waiting_text = State()

class TeacherAnnounceState(StatesGroup):
    waiting_text = State()

class TuitionState(StatesGroup):
    waiting_group_for_amount = State()
    waiting_amount = State()

class AdminAIState(StatesGroup):
    chatting = State()
