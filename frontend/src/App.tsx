import { useState, useEffect } from "react";

interface ChatItem {
  question: string;
  type: string;
}

const App = () => {
  const [open, setOpen] = useState(true);
  const [result, setResult] = useState("");
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [chatHistory, setChatHistory] = useState<ChatItem[]>([]);
  const [uploadStatus, setUploadStatus] = useState(false); // State variable for tracking upload status

  const handleQuestionChange = (event: any) => {
    setQuestion(event.target.value);
  };

  const handleFileChange = (event: any) => {
    setFile(event.target.files[0]);
    setUploadStatus(true); // Set upload status to true when file is uploaded
  };

  const handleKeyPress = (event: any) => {
    if (event.key === "Enter") {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    const formData = new FormData();

    if (file) {
      formData.append("file", file);
    }
    if (question) {
      formData.append("question", question);
    }
    if (!question) return;

    setChatHistory((prevHistory) => [
      ...prevHistory,
      { question, type: "You" },
    ]);
    setQuestion("");

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setChatHistory((prevHistory) => [
        ...prevHistory,
        { question: data.result, type: "Chatbot" },
      ]);
    } catch (error) {
      console.error("Error", error);
    }
  };

  useEffect(() => {
    // Hide pop-up after 3 seconds
    if (uploadStatus) {
      const timer = setTimeout(() => {
        setUploadStatus(false);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [uploadStatus]);

  return (
    <div className="flex">
      <div
        className={` ${
          open ? "w-1/2" : "w-0 "
        } bg-dark-purple h-screen p-5  pt-8 relative duration-300 mr-11`}
      >
        <div className="flex gap-x-4 items-center">
          <h1
            className={`text-white origin-left font-medium text-xl duration-200 p-4 ${
              !open && "scale-0"
            }`}
          >
            ChatBot
          </h1>
        </div>

        <ul className="bg-slate-50 p-4 sm:px-8 sm:pt-6 sm:pb-8 lg:p-4 xl:px-8 xl:pt-6 xl:pb-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2 gap-4 text-sm leading-6 rounded-3xl pt-8 mt-11">
          <div className="appBlock content rounded-3xl">
            <div className="flex items-center justify-between">
              <label
                htmlFor="file"
                className="hover:border-blue-500 hover:border-solid hover:bg-white hover:text-blue-500 group w-full flex flex-col items-center justify-center rounded-md border-2 border-dashed border-slate-300 text-sm leading-6 text-slate-900 font-medium py-3 rounded-3xl"
              >
                <svg
                  className="group-hover:text-blue-500 mb-1 text-slate-400 rounded-3xl"
                  width="20"
                  height="20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M10 5a1 1 0 0 1 1 1v3h3a1 1 0 1 1 0 2h-3v3a1 1 0 1 1-2 0v-3H6a1 1 0 1 1 0-2h3V6a1 1 0 0 1 1-1Z" />
                </svg>
                Upload Your File
                <input
                  type="file"
                  id="file"
                  name="file"
                  accept=".txt, .pdf, .csv, .docx"
                  onChange={handleFileChange}
                  className="fileInput sr-only"
                />
              </label>
            </div>
          </div>
        </ul>
      </div>

      <div className="flex flex-col text-center w-full justify-content: center">
        {chatHistory.map((chat, index) => (
          <div
            key={index}
            className={`pt-6 pl-6 max-w-96 ${
              chat.type === "Chatbot" ? "float-right mr-12" : "float-left ml-12"
            }`}
          >
            <h1 className="text-2xl font-semibold ">
              <figure
                className={`md:flex rounded-xl p-8 md:p-0 ${
                  chat.type === "Chatbot"
                    ? "bg-slate-800"
                    : "bg-sky-500 dark:bg-sky-500"
                }`}
              >
                <div className="pt-3 md:p-3 space-y-8">
                  <blockquote>
                    <p
                      className={`resultOutput text-sm font-semibold ${
                        chat.type === "Chatbot"
                          ? "text-white text-left pb-2 bg-slate-600 rounded-3xl pl-5 pt-2"
                          : "text-white text-left pb-2 bg-sky-400 rounded-3xl pl-5 pt-2"
                      }`}
                    >
                      {chat.type}
                    </p>
                    <p
                      className={`resultOutput text-sm font-semibold ${
                        chat.type === "Chatbot"
                          ? "text-white text-left pt-3 pl-5 pr-5 pb-2"
                          : "text-white text-left pt-3 pl-5 pr-5 pb-2"
                      }`}
                    >
                      {chat.question}
                    </p>
                  </blockquote>
                </div>
              </figure>
            </h1>
          </div>
        ))}
      </div>

      <div>
        <div className="fixed w-full bottom-0 right-0 left-0 bg-gray-900 border-t border-gray-600 p-4 flex items-center pt-12 pb-12 pr-12 pl-12">
          <input
            type="text"
            className="flex-grow px-4 py-3 border rounded-md focus:outline-none focus:border-blue-500 bg-gray-800 text-white mr-4"
            placeholder="Type here..."
            value={question}
            onChange={handleQuestionChange}
            onKeyDown={handleKeyPress}
          />
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none"
            onClick={handleSubmit}
            disabled={!question}
          >
            Send
          </button>
          {/* Display pop-up when file is uploaded */}
          {uploadStatus && (
            <div className="absolute bottom-10 right-10 bg-white text-black p-4 rounded-md">
              File uploaded successfully!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
