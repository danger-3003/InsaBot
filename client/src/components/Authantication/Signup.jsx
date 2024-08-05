import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [jump, setJump] = useState()

    const handleLogin = () => {
        window.alert('it may take some time')
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        console.log(formData.username)
        // axios.post('http://localhost:8000/register/', formData)
        //     .then(response => {
        //         console.log('Success:', response.data);
        //         setJump(true)
        //     })
        //     .catch(error => {
        //         console.error('Error:', error);
        //         setJump(false)
        //     });
    };
    return (
        <div className='flex bg-zinc-900 gap-16 items-center text-white flex-col login_box mt-14 rounded-xl'>
            <h1 className='title absolute text-4xl mt-10 text-white'>Insta</h1>
            <div className='flex mt-28 gap-4 flex-col'>
                <input
                    type="text"
                    className='rounded-md py-2 px-4 bg-zinc-700 placeholder:text-black'
                    placeholder="Username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />

                <input
                    type="password"
                    className='rounded-md py-2 px-4 bg-zinc-700 placeholder:text-black'
                    placeholder="Password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
            </div>
            <button
                // style={jump ? { display: 'none' } : { display: 'block' }}
                className='px-24 py-2 rounded-md bg-white text-black'
                onClick={handleLogin}
            >
                Signup
            </button>
            {jump ? <span></span> : <span className='text-red-200'>Your Instagram login credential must match to it</span>}
            {/* {jump &&
            <Link to='http://localhost:5174/Home/'>

                <div className='flex flex-col'><button
                    className='px-24 py-2 rounded-md bg-white text-black'
                >
                    Move to Home
                </button>
                    <span>Signup Successfull</span>
                </div>
            </Link>
            } */}
            <div className="flex">
                <span className="line">___________</span>
                <span className='mx-2'>OR</span>
                <span className="line">___________</span>
            </div>
            <Link to='http://localhost:5174'>
                <div className="flex">
                    <span>Already have an account?</span>
                    <span> Login</span>
                </div>
            </Link>
        </div>
    );
};

export default Signup ;
