import { useState } from "react";
import axios from 'axios';

function Follow() {
    const [value, setValue] = useState("");
    const [counter,setCounter] = useState(false);
    const [loader, setLoader] = useState(false);
    const [error, setError] = useState(false);
    const handleInput = (event) => {
        setValue(event.target.value);
    };
    const handleSubmit = (event) => {
        event.preventDefault();
        setLoader(true);
        axios.post('http://127.0.0.1:8000/follow_user',{usernameToFollow:value})
        .then((res)=>{
            setCounter(true);
            setLoader(false);
            setTimeout(() => {
                setCounter(false);
            }, 3000);
        })
        .catch((err)=>{
            setError(true);
            setTimeout(() => {
                setLoader(false);
                setError(false);
            }, 3000);
        });
        event.target.reset();
        setValue("");
    };
    return (
        <div className="w-full">
            <div className="bg-black rounded">
                <form className="max-w-md mx-auto mt-8 p-6 text-black" onSubmit={handleSubmit}>
                    <label htmlFor="inputField" className="block text-gray-400">
                        Enter user ID:
                    </label>
                    <input
                        type="text"
                        id="inputField"
                        onChange={handleInput}
                        className="mt-2 p-2 border border-gray-300 bg-gray-600 text-white rounded w-full focus:outline-none focus:border-blue-500"
                    />
                    <p className="text-gray-400 mt-2">user to follow: <span className="text-red-300">{value}</span></p>
                    <button
                        type="submit"
                        className="text-white self-center bg-gradient-to-br w-[50%] from-pink-500 to-orange-400 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mt-4"
                    >
                        Follow
                    </button>
                </form>
            </div>
            {counter &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">You have followed {value}</p>
                </div>
            }
            {loader &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] animate-pulse h-screen">
                    <p className="text-slate-800 bg-white p-10">Loading...</p>
                </div>
            }
            {error &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">Error in following {value}</p>
                </div>
            }
        </div>
    );
}

export default Follow;
