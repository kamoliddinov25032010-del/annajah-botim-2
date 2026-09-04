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
