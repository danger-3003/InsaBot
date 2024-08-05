import { useState } from "react";
import axios from "axios";

function Message() {
    const [inputValue, setInputValue] = useState("");
    const [message, setMessage] = useState("");
    const [loader, setLoader] = useState(false);
    const [error, setError] = useState(false);
    const [counter, setCounter] = useState(false);

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        setLoader(true);
        const inputArray = inputValue.split(",");
        console.log(inputArray, message);
        axios
            .post("http://localhost:8000/message_to_multiple_users", {
                lst: inputArray,
                msg: message,
            })
            .then(() => {
                setLoader(false);
                setCounter(true);
                setTimeout(() => {
                    setCounter(false);
                }, 3000);
            })
            .catch(() => {
                setError(true);
                setTimeout(() => {
                    setError(false);
                    setLoader(false);
                }, 3000);
            });
        e.target.reset();
        setInputValue("");
    };

    return (
        <>
            <form onSubmit={handleSubmit}>
                <div className="bg-black p-3 rounded-md ">
                    <div>
                        <div className="max-w-md mx-auto mt-8 p-6 text-black">
                            <label
                                htmlFor="inputField"
                                className="block text-gray-400"
                            >
                                Enter multiple Id's (separated by commas):
                            </label>
                            <input
                                type="text"
                                id="inputField"
                                onChange={handleInputChange}
                                className="mt-2 p-2 border border-gray-300 rounded w-full focus:outline-none focus:border-blue-500"
                            />

                            {/* Display current inputs */}
                            <div className="mt-4 flex gap-2 text-gray-200">
                                <strong className=" mb-2 text-gray-200">
                                    Current inputs :
                                </strong>
                                {inputValue}
                            </div>
                        </div>
                    </div>
                    <label className="sr-only">Your message</label>
                    <div className="flex items-center px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-700">
                        <textarea
                            onChange={(e) => setMessage(e.target.value)}
                            id="chat"
                            rows="1"
                            className="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Your message..."
                        ></textarea>
                        <button
                            type="submit"
                            className="inline-flex justify-center p-2 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600"
                        >
                            <svg
                                className="w-5 h-5 rotate-90 rtl:-rotate-90"
                                aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="currentColor"
                                viewBox="0 0 18 20"
                            >
                                <path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z" />
                            </svg>
                        </button>
                    </div>
                </div>
            </form>
            {counter && (
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">
                        You have messaged {inputValue}
                    </p>
                </div>
            )}
            {loader && (
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] animate-pulse h-screen">
                    <p className="text-slate-800 bg-white p-10">Loading...</p>
                </div>
            )}
            {error && (
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">
                        Error in messaging {inputValue}
                    </p>
                </div>
            )}
        </>
    );
}

export default Message;
