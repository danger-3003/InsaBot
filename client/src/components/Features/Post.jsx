import { useState } from "react";
import axios from "axios";

function Post() {
    const [caption, setCaption] = useState("");
    const [file, setFile] = useState(null);
    const [counter,setCounter] = useState(false);
    const [loader, setLoader] = useState(false);
    const [error, setError] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleCaptionChange = (event) => {
        setCaption(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append("file", file);
        formData.append("caption", caption);
        setLoader(true);
        axios.post(`http://localhost:8000/upload_post?caption=${encodeURIComponent(caption)}`,formData,{
            headers:{
            'Content-Type': 'multipart/form-data',
            }
        })
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
            <div className="bg-black p-3 rounded-md ">
                {/* Main form container */}
                <form className="flex gap-2 flex-col" onSubmit={handleSubmit}>
                    <div className="flex flex-wrap justify-between">
                        {/* Left column */}
                        <div className="flex flex-col gap-3">
                            {/* File upload input */}
                            <input
                                required
                                type="file"
                                onChange={handleFileChange}
                                className="block w-full text-sm text-gray-500 file:me-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:disabled:opacity-50 file:disabled:pointer-events-none dark:text-neutral-500 dark:file:bg-blue-500 dark:hover:file:bg-blue-400"
                            ></input>
                        </div>
                        {/* Right column */}
                    </div>
                    {/* Caption textarea */}
                    <div className="px-4 py-2 bg-white rounded-lg dark:bg-gray-800">
                        <label htmlFor="comment" className="sr-only">
                            Your comment
                        </label>
                        <textarea
                            id="comment"
                            rows="4"
                            onChange={handleCaptionChange}
                            className="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white focus:outline-none dark:placeholder-gray-400"
                            placeholder="Write a caption..."
                        ></textarea>
                    </div>
                    {/* Submit button */}
                    <button
                        type="submit"
                        className="text-white self-center bg-gradient-to-br w-[50%] from-pink-500 to-orange-400 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"
                    >
                        Post Now
                    </button>
                </form>
            </div>
            {counter &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">Posted</p>
                </div>
            }
            {loader &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] animate-pulse h-screen">
                    <p className="text-slate-800 bg-white p-10">Loading...</p>
                </div>
            }
            {error &&
                <div className="bg-[#00000070] absolute top-0 left-0 w-[100%] h-screen">
                    <p className="text-slate-800 bg-white p-10">Error in uploading the post..</p>
                </div>
            }
        </>
    );
}

export default Post;
