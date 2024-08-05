import { useState } from "react";
import { IoGlobe } from "react-icons/io5";
import axios from "axios";

function Like() {
    const [url, setUrl] = useState("");
    const [counter,setCounter] = useState(false);
    const [loader, setLoader] = useState(false);
    const [error, setError] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoader(true)
        axios.post('http://127.0.0.1:8000/like_post',{post_url:url})
        .then((res)=>{
            setCounter(true);
            setLoader(false);
            setTimeout(() => {
                setCounter(false);
            }, 3000);
        })
        .catch((err)=>{
            setError(true);
            setTimeout(()=>{
                setLoader(false);
                setError(false);
            },3000)
        });
    };
    return (
        <>
            <div className="bg-black p-3 rounded-md">
                <form className="flex gap-2 flex-col" onSubmit={handleSubmit}>
                    {/* Input field for website URL */}
                    <div className="flex justify-between">
                        <div className="flex flex-col gap-3">
                            <div className="flex">
                                {/* Globe icon */}
                                <span className="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border rounded-l-md border-gray-300 dark:bg-gray-600 dark:text-gray-400 dark:border-gray-600">
                                    <IoGlobe />
                                </span>
                                {/* URL input field */}
                                <input
                                    type="url"
                                    id="website-admin"
                                    className="focus:outline-none rounded-none rounded-r-lg bg-gray-50 border text-gray-900 w-56 text-sm border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                                    placeholder="url: https://instagram.com/example_123/"
                                    onChange={e=>setUrl(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Like button */}
                    <button
                        type="submit"
                        className="text-white self-center bg-gradient-to-br w-[50%] from-pink-500 to-orange-400 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mt-4"
                    >
                        Like
                    </button>
                </form>
            </div>
            {counter &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">Liked the post</p>
                </div>
            }
            {loader &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] animate-pulse h-screen">
                    <p className="text-slate-800 bg-white p-10">Loading...</p>
                </div>
            }
            {error &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">Error in liking the post..</p>
                </div>
            }
        </>
    );
}

export default Like;
