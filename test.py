from evernote.api.client import EvernoteClient
from config import developer_token

# Set up the NoteStore client 
client = EvernoteClient(token=developer_token, sandbox=False, china=True)
note_store = client.get_note_store()
 
# Make API calls
notebooks = note_store.listNotebooks()
for notebook in notebooks:
    print("Notebook: ", notebook.name)