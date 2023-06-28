import logging, json

from constants import SETTINGS_FILE_PATH

LLM_URL = "http://localhost:5000"

LLM_USERNAME = None

LLM_PASSWORD = None

EMBEDDING_MODEL_NAME = "hkunlp/instructor-large"

class Settings:
  def __init__(self, enableTextGenWebui, textGenWebuiURL, textGenWebuiEnableAuth,
               textGenWebuiUsername, textGenWebuiPassword, openaiEnabled, opeanAIApiKey):
    self.enableTextGenWebui = enableTextGenWebui
    self.textGenWebuiURL = textGenWebuiURL
    self.textGenWebuiEnableAuth = textGenWebuiEnableAuth
    self.textGenWebuiUsername = textGenWebuiUsername
    self.textGenWebuiPassword = textGenWebuiPassword
    self.openaiEnabled = openaiEnabled
    self.opeanAIApiKey = opeanAIApiKey

  def to_json(self):
    return json.dumps(self.__dict__)

  @classmethod
  def from_json(cls, json_data):
    data = json.loads(json_data)
    return cls(**data)

CURRENT_SETTINGS = Settings(True, "http://localhost:5000",False, "", "", False,"PUT YOUR API KEY HERE")

def read_string_from_file(file_path):
  try:
    with open(file_path, 'r') as file:
      return file.read()
  except Exception:
    return None

def write_string_to_file(file_path, content):
  with open(file_path, 'w') as file:
    file.write(content)

def saveSettings(settings):
  write_string_to_file(SETTINGS_FILE_PATH, settings.to_json())
  logging.info(f"Settings saved to {SETTINGS_FILE_PATH}")

def loadSettings():
  global CURRENT_SETTINGS
  settings = read_string_from_file(SETTINGS_FILE_PATH)
  if settings is None:
    logging.info("Settings file not found! using default.")
  else:
    CURRENT_SETTINGS = Settings.from_json(settings)
  return CURRENT_SETTINGS

def getSettings():
  global CURRENT_SETTINGS
  return CURRENT_SETTINGS