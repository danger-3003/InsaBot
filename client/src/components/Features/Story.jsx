import {useState} from 'react';

function Story() {

  const [file,setFile]=useState("");
  const [caption,setCaption]=useState("");

  const handleSubmit=(e)=>{
    e.preventDefault();
    console.log(file,caption);
  }

  return (
    <div className='bg-black rounded p-2'>
      {/* Main form container */}
      <form className='flex gap-2 flex-col' onSubmit={handleSubmit}>
        <div className='flex flex-wrap justify-between'>
          {/* Left column */}
          <div className='flex flex-col gap-3 '>
            {/* File input */}
            <input onChange={e=>setFile(e.target.value)} type="file" className="block w-full text-sm text-gray-500 file:me-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:disabled:opacity-50 file:disabled:pointer-events-none dark:text-neutral-500 dark:file:bg-blue-500 dark:hover:file:bg-blue-400" />
          </div>
        </div>
        <div className="flex w-full">
              <input onChange={e=>setCaption(e.target.value)} type="text" id="website-admin" className="w-full focus:outline-none rounded bg-gray-50 border text-gray-900 flex w-26 text-sm border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white" placeholder="caption" />
          </div>
        {/* Submit button */}
        <button type="submit" className="text-white self-center bg-gradient-to-br w-[50%] from-pink-500 to-orange-400 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">Post Now</button>
      </form>
    </div>
  );
}

export default Story;
