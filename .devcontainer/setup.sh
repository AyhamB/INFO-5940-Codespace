sudo apt-get update 
sudo apt-get install -y \
    curl \
    git \
    unzip \
    vim \
    wget \
    gcc \

pip install -r requirements.txt
ARCHFLAGS="-arch x86_64" pip install "chromadb>=0.5" langchain_chroma langgraph

# curl "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o "awscliv2.zip" \
#     && unzip -o awscliv2.zip \
#     && sudo ./aws/install --update \
#     && echo 'complete -C '/usr/local/bin/aws_completer' aws' >> ~/.bashrc \
#     && rm -rf awscliv2.zip ./aws


