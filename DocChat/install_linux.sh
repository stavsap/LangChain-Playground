git clone https://github.com/stavsap/LangChain-Playground.git
cd LangChain-Playground/DocChat
python3 -m venv venv
source venv/bin/activate
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
python -m pip install -r requirements.txt
chmod +x run_linux.sh
./run_linux.sh
