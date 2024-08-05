import React, {useState} from "react";
import { IoGlobe } from "react-icons/io5";
import axios from "axios";

function Comment() {
    const [post_url,setpost_url]=useState("");
    const [comment_text,setcomment_text]=useState("");
    const [counter,setCounter] = useState(false);
    const [loader, setLoader] = useState(false);
    const [error,setError] =useState(false);

    const handleSubmit=(e)=>{
        e.preventDefault();
        setLoader(true);
        axios.post('http://127.0.0.1:8000/comment_on_post',{post_url:post_url,comment_text:comment_text})
        .then((res)=>{
            if(res){
                setCounter(true);
                setLoader(false);
                setTimeout(() => {
                    setCounter(false);
                }, 3000);
            }
        })
        .catch((err)=>{
            if (err){
                setError(true);
                setTimeout(() => {
                    setError(false);
                    setLoader(false);
                }, 3000);
            }
        });
        e.target.reset();
    }

    return (
        <div>
            <div className="bg-black p-3 rounded-md">
                <form className="flex gap-2 flex-col" onSubmit={handleSubmit}>
                    {/* Website URL input */}
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
                                    onChange={(e)=>setpost_url(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Comment textarea */}
                    <div className="px-4 py-2 bg-white rounded-lg dark:bg-gray-800">
                        <label htmlFor="comment" className="sr-only">
                            Your comment
                        </label>
                        <textarea
                            id="comment"
                            rows="4"
                            className="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:text-white dark:bg-gray-800 focus:ring-0 focus:outline-none dark:placeholder-gray-400"
                            placeholder="Write Comment..."
                            required
                            onChange={(e)=>setcomment_text(e.target.value)}
                        ></textarea>
                    </div>

                    {/* Submit button */}
                    <button
                        type="submit"
                        className="text-white self-center bg-gradient-to-br w-[50%] from-pink-500 to-orange-400 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"
                    >
                        Comment Now
                    </button>
                </form>
            </div>
            {counter &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">Commented successfully</p>
                </div>
            }
            {loader &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] animate-pulse h-screen">
                    <p className="text-slate-800 bg-white p-10">Loading...</p>
                </div>
            }
            {error &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">Error in commenting the post</p>
                </div>
            }
        </div>
    );
}

export default Comment;
