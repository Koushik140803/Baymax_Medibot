# Baymax Medibot

Baymax Medibot is an AI-powered healthcare assistant inspired by the concept of Baymax from Disney's "Big Hero 6." This project leverages the power of FLAN-T5 for natural language generation and FAISS for efficient retrieval-augmented generation (RAG). It provides an intuitive interface built with Streamlit (frontend) and FastAPI (backend).  
__Addressing few things__: the complete folder structure i have not provided. Hence you have to add these file to a folder containing all the datasets, model files (using locally) and replace them in the code.  
__Note__: model response it entirely based on how well you finetune it since flan-t5 asks for more data when domain specific responses are required.  

## Features
- **FLAN-T5-based AI Model**: Generates meaningful responses tailored to user queries.
- **FAISS RAG Implementation**: Efficient retrieval of context-relevant information.
- **Frontend with Streamlit**: Simple and user-friendly interface for interaction.
- **Backend with FastAPI**: Robust backend to handle data processing and API requests.

## Folder Structure
```
Baymax_Medibot_App/
├── main.ipynb      # Jupyter Notebook containing code for data preprocessing, RAG setup, and model fine-tuning
├── app.py          # Streamlit frontend file
├── backend.py      # FastAPI backend file
```

## Requirements
### System Requirements
To ensure the project runs smoothly, your system should meet the following requirements:
- **Operating System**: Windows 10/11, macOS 10.15+, or any Linux distribution
- **Processor**: Intel i5 (6th gen or above), AMD Ryzen 5, or equivalent
- **Memory**: Minimum 8 GB of RAM (16 GB recommended)
- **Storage**: At least 5 GB of free disk space
- **GPU (Optional)**: NVIDIA GPU with CUDA support for faster model inference (e.g., GTX 1060 or above)

### Software Requirements
- **Python**: Version 3.8 or higher
- Libraries: 
  - `transformers`
  - `faiss`
  - `fastapi`
  - `uvicorn`
  - `streamlit`
  - Other standard Python libraries (specified in the notebook or backend code)

## Installation and Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Koushik140803/Baymax_Medibot.git
   cd Baymax_Medibot_App
   ```

2. **Install Required Libraries**:
   Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Backend**:
   Start the FastAPI backend:
   ```bash
   uvicorn backend:app --reload
   ```

4. **Run the Frontend**:
   Start the Streamlit frontend:
   ```bash
   streamlit run app.py
   ```

5. **Interact with Baymax Medibot**:
   Open your browser and navigate to the Streamlit interface to interact with the bot.

## How It Works
1. **Data Preprocessing**:  
   The `main.ipynb` file includes preprocessing steps to prepare the data for training and retrieval.

2. **RAG Setup**:  
   The notebook demonstrates the integration of FAISS for retrieval-augmented generation, enhancing the model's ability to provide accurate responses.

3. **Model Fine-Tuning**:  
   The FLAN-T5 model is fine-tuned on domain-specific data for optimal performance.

4. **Backend**:  
   The FastAPI backend serves as the API layer, handling model inference and data requests.

5. **Frontend**:  
   The Streamlit frontend provides an easy-to-use interface for users to interact with the AI assistant.

## Future Scope
- Add more domain-specific datasets for improved accuracy.
- Integrate advanced features like speech-to-text and text-to-speech for better accessibility.
- Deploy the application on a cloud platform for wider accessibility.

## Contributing
Contributions are highly valued as this project is an initial attempt at recreating Baymax, with significant potential for further enhancements and considerations. If you have ideas for new features or improvements, please fork the repository and submit a pull request.  

## License
This project is licensed under the [MIT License](LICENSE).

---

Feel free to reach out if you have any questions or suggestions for improving Baymax Medibot!
