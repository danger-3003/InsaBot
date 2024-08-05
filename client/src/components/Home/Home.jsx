import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '../Navbar';
import './Home.css';
import { FaHeart } from "react-icons/fa";
import { RiUserFollowFill } from "react-icons/ri";
import { BsFilePost } from "react-icons/bs";
import { AiFillMessage } from "react-icons/ai";
import { FaCameraRetro } from "react-icons/fa";
import { FaCommentDots } from "react-icons/fa";
import Like from '../Features/Like';
import Story from '../Features/Story';
import Message from '../Features/Message';
import Follow from '../Features/Follow';
import Comment from '../Features/Comment';
import Post from '../Features/Post';

function Home() {
    const location = useLocation();
    const navigate = useNavigate();
    const userDetails = location.state || {username:"", password:""};
    const [selectedOption, setSelectedOption] = useState('Follow');

    useEffect(()=>{
        if(userDetails.username=="")
        {
            navigate("/");
        }
    })

    const handleLogout =() =>{
        navigate("/")
    }

    // Functions to handle card clicks
    const card_follow = () => {
        setSelectedOption('Follow');
    };
    const card_story = () => {
        setSelectedOption('Story');
    };
    const card_like = () => {
        setSelectedOption('Like');
    };
    const card_comment = () => {
        setSelectedOption('Comment');
    };
    const card_message = () => {
        setSelectedOption('Message');
    };
    const card_post = () => {
        setSelectedOption('Post');
    };

    // Function to handle select change
    const onChangeOption = (event) => {
        setSelectedOption(event.target.value);
    };

    return (
        <div className='h-screen text-white w-full'>
            <Navbar />
            <div className='flex pt-10 px-8 justify-between'>
                {/* <div className='flex flex-col gap-2'>
                    <h3 className='p-2 py-1 rounded-full bg-sky-100 text-black'>Followers: <span className=''>20</span></h3>
                    <h3 className='p-2 py-1 w-fit rounded-full bg-red-100 text-black'>Likes: <span className=''>20</span></h3>
                </div> */}
                <div>
                    <button onClick={handleLogout}>LogOut</button>
                </div>
                <div className='text-right'>
                    <h3>{userDetails.username}</h3>
                </div>
            </div>
            <div className='flex flex-wrap h-96 justify-evenly'>
                <div className="home_page p-6 py-6 gap-5 flex flex-wrap">
                    {/* Follow card */}
                    <div onClick={card_follow} className="card p-2 relative">
                        <RiUserFollowFill className='text-blue-600 text-2xl absolute top-2 right-2' />
                        <h3 className='text-zinc-600'>Do follow, <br />to multiple profile</h3>
                        <h2 className='absolute bottom-3 text-3xl font-semibold left-2'>Follow</h2>
                    </div>
                    {/* Story card */}
                    {/* <div onClick={card_story} className="card p-2 relative">
                        <FaCameraRetro className='text-red-600 text-2xl absolute top-2 right-2' />
                        <h3 className='text-zinc-600'>Keep story, <br />on your profile</h3>
                        <h2 className='absolute bottom-3 text-3xl font-semibold left-2'>Story</h2>
                    </div> */}
                    {/* Comment card */}
                    <div onClick={card_comment} className="card p-2 relative">
                        <FaCommentDots className='text-emerald-600 text-2xl absolute top-2 right-2' />
                        <h3 className='text-zinc-600'>Do comment, <br /> on someone's post</h3>
                        <h2 className='absolute bottom-3 text-3xl font-semibold left-2'>Comment</h2>
                    </div>
                    {/* Like card */}
                    <div onClick={card_like} className="card p-2 relative">
                        <FaHeart className='text-red-600 text-2xl absolute top-2 right-2' />
                        <h3 className='text-zinc-600'>Like multiple, <br /> posts at a time</h3>
                        <h2 className='absolute bottom-3 text-3xl font-semibold left-2'>Like</h2>
                    </div>
                    {/* Message card */}
                    <div onClick={card_message} className="card p-2 relative">
                        <AiFillMessage className='text-sky-600 text-2xl absolute top-2 right-2' />
                        <h3 className='text-zinc-600'>Send multiple, <br /> Messages at a time</h3>
                        <h2 className='absolute bottom-3 text-3xl font-semibold left-2'>Message</h2>
                    </div>
                    {/* Post card */}
                    <div onClick={card_post} className="card p-2 relative">
                        <BsFilePost className='text-green-600 text-2xl absolute top-2 right-2' />
                        <h3 className='text-zinc-600'>Post something,<br />on your profile</h3>
                        <h2 className='absolute bottom-3 text-3xl font-semibold left-2'>Post</h2>
                    </div>
                </div>
                {/* Activity section */}
                <div className='activity bg-white'>
                    <div className='flex items-center border-b-[1px] mb-4 pb-3 justify-between'>
                        <div>
                            <h3 className='text-md text-gray-500'>Activity</h3>
                            <h2 className='text-xl text-black font-semibold'>{selectedOption}</h2>
                        </div>
                        {/* Dropdown for selecting activity */}
                        <div>
                            <select
                                id="options"
                                value={selectedOption}
                                onChange={onChangeOption}
                                className="mt-1 block w-full text-black p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none sm:text-sm">
                                <option value="Follow">Follow</option>
                                <option value="Comment">Comment</option>
                                <option value="Like">Like</option>
                                <option value="Message">Message</option>
                                <option value="Post">Post</option>
                                <option value="Story">Story</option>
                            </select>
                        </div>
                    </div>
                    {/* Render selected component based on selectedOption */}
                    {selectedOption === 'Like' && <Like />}
                    {selectedOption === 'Follow' && <Follow />}
                    {selectedOption === 'Post' && <Post />}
                    {selectedOption === 'Story' && <Story />}
                    {selectedOption === 'Comment' && <Comment />}
                    {selectedOption === 'Message' && <Message />}
                </div>
            </div>
        </div>
    );
}

export default Home;
