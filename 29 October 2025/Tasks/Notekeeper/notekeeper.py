import streamlit as st

# Initialize session state
if "notes" not in st.session_state:
    st.session_state["notes"] = []

# Streamlit UI
st.set_page_config(page_title="NoteKeeper Tool", page_icon="🗒️")
st.title("🗒️ NoteKeeper Agent")

# Input for new note
note_input = st.text_input("Add a new note (you can include tags like #work, #personal):")

if st.button("Save Note"):
    if note_input.strip():
        st.session_state["notes"].append(note_input.strip())
        st.success(f'Agent: Noted — “{note_input.strip()}”')
    else:
        st.warning("Please enter a valid note.")

# Search/filter section
st.subheader("🔍 Search Notes")
search_query = st.text_input("Search by keyword or tag (e.g., 'email', '#work'):")

if search_query:
    filtered_notes = [note for note in st.session_state["notes"] if search_query.lower() in note.lower()]
    if filtered_notes:
        st.write(f"Found {len(filtered_notes)} matching note(s):")
        for i, note in enumerate(filtered_notes, start=1):
            st.write(f"{i}. {note}")
    else:
        st.info("No matching notes found.")

# Display all notes
st.subheader("📋 All Notes")
if st.session_state["notes"]:
    for i, note in enumerate(st.session_state["notes"], start=1):
        st.write(f"{i}. {note}")
else:
    st.info("You currently have no notes.")