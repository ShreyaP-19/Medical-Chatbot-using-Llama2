**End-to-End Medical ChatBot using Llama2**

*Clone the project*

**Step 1-Create a conda environment after opening the repository**

>conda create -n mchatbot python=3.8 -y
>conda activate mchatbot

**Step 2-Install the requirements**

>pip install -r requirements.txt

**Step 3-Create a '.env' file in the root directory and add your pincone credentials as follows:**

>PINECONE_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

**Step 4-Download the quantize model from the link provided in model folder & keep the model in the model directory:**

>llama-2-7b-chat.ggmlv3.q4_0.bin
*From:*
>https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q4_0.bin

**Step 5-Store the vectors**
>python store_index.py

**Step 6-Run the app**
>python app.py

**TECHSTACK USED:**
*Python*
*LangChain*
*Flask*
*Meta Llama2*
*Pinecone*