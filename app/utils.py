
def format_note_id(note_id: int) -> str:
    return str(note_id).zfill(5)

def format_date(date_obj) -> str:

    return date_obj.strftime("%d.%m.%Y")

def build_note_response(note, login: str) -> dict:

    return {
        "id": format_note_id(note.note_id),
        "title_user": f"{note.title} - {login}",
        "content": note.content,
        "formatted_date": format_date(note.created_at),
    }