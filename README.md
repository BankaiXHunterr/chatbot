# Running the Chatbot Application

Congratulations on completing the ProtonDatalabs AI Developer Assignment! Below are the instructions to follow to run the application, along with an explanation of the choices made during development.

## Instructions

### Backend Setup:

1. **Obtain API Key**: Obtain the API key required for the Google services. This key will be used for language modeling and other functionalities.

2. **Environment Setup**: 
   - Create an `.env` file inside the `backend` folder.
   - Store the obtained API key as `GOOGLE_API_KEY`[https://aistudio.google.com/app/prompts/new_chat] within the `.env` file.

3. **Python Environment Setup**: 
   - Ensure Python 3.10 or above is installed on your system.
   - Use Conda package manager to set up a virtual environment named `chatbot`:
     ```
     conda create -n chatbot python=3.10
     conda activate chatbot
     ```

4. **Install Dependencies**: 
   - Navigate to the `backend` directory in the terminal.
   - Install the required Python packages using pip:
     ```
     pip install -r requirements.txt
     ```

5. **Running the Backend Server**: 
   - In the terminal, navigate to the `backend` directory.
   - Execute the following command to start the FastAPI server:
     ```
     uvicorn main:app --reload
     ```

   The server will start running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Frontend Setup:

1. **Node.js Installation**: 
   - Ensure Node.js v20.11.1 or above is installed on your system.
   - You can download and install Node.js from [here](https://nodejs.org/en/).

2. **Environment Setup**:
   - Open a new terminal window.

3. **Navigate to Frontend Directory**: 
   - In the terminal, navigate to the `frontend` directory of the project.

4. **Install Dependencies**:
   - Run the following command to install the required Node.js dependencies:
     ```
     npm install
     ```

5. **Launch the React App**: 
   - After installing dependencies, run the following command to start the development server:
     ```
     npm start
     ```

   This will open the application in your default web browser at [http://localhost:3000](http://localhost:3000/).

## Explanation of Choices

### Technology Stack:

- **Language Models (LLMs)**: 
  - Utilized Langachain and Google Gemini for natural language processing tasks due to their robustness and performance.

- **Vectorization and Storage**: 
  - Employed FAISS for vectorization and vector storage. FAISS offers efficient and scalable solutions for similarity search tasks.

- **Styling**: 
  - Chose Tailwind CSS for styling due to its utility-first approach, which enables rapid development and easy customization.

### Backend Decisions:

- **FastAPI**: 
  - Chose FastAPI for backend development due to its high performance, asynchronous support, and automatic API documentation generation.

- **API Key Handling**: 
  - Stored the Google API key securely in an environment variable to ensure sensitive information is not exposed in the codebase.

### Frontend Decisions:

- **React Framework**: 
  - Selected React for frontend development to build a dynamic and interactive user interface.

- **File Upload Handling**: 
  - Implemented support for multiple file formats (.txt, .docx, .pdf, .csv) to enhance user flexibility and accommodate different types of documents.

- **Styling Framework**: 
  - Opted for Tailwind CSS for styling to maintain consistency and ease of development, allowing for rapid prototyping and responsive design.

By following these instructions, you should be able to run the chatbot application successfully and experience its functionalities firsthand. If you encounter any issues or have further questions, feel free to reach out for assistance. Happy coding!
