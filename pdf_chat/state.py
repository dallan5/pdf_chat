class StateManager:
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super(StateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._pdf_path = ""
        self._source_text = ""
        self._conversation_messages = list()
        self._system_messages = list()

    @property
    def pdf_path(self):
        return self._pdf_path
    
    @pdf_path.setter
    def pdf_path(self, path):
        self._pdf_path = path

    @property
    def source_text(self):
        return self._source_text

    @source_text.setter
    def source_text(self, text):
        self._source_text = text
        print("source_text SET")
        print(self._source_text)
        print('---------------------')

    @property
    def system_messages(self):
        return self._system_messages

    @system_messages.setter
    def system_messages(self, messages):
        self._system_messages = messages
        print("SYSTEM MESSAGES SET")
        print(self._system_messages)
        print('---------------------')

    @property
    def conversation_messages(self):
        return self._conversation_messages

def get_state_manager():
    return StateManager()
