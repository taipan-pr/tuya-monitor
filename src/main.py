from process import Process
from dotenv import find_dotenv, load_dotenv

print(f"Process start")

# load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

process = Process()
process.process()
