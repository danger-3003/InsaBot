import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error,setError] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault(); // Verify the data being sent
        setLoading(true);
        axios
            .post("https://instabot-ddde.onrender.com/check_login", {
                username: username,
                password: password,
            }) // No need to stringify the values
            .then((response) => {
                console.log(response);
                navigate('/home',{state:{username,password}});
                setUsername("");
                setPassword("");
            })
            .catch((error) => {
                console.log("Error", error.message);
                setLoading(false)
                setError(true);
                setTimeout(() => {
                    setError(false);
                }, 5000);
            });
        event.target.reset();
    };

    return (
        <div className="flex items-center h-fit text-white mt-16 flex-col login_box bg-zinc-900 rounded-xl">
            <h1 className="title text-4xl mt-10 mb-5 text-white">Insta Bot</h1>
            <p className="mb-5">Please use instagram credentials only</p>
            <form action="" onSubmit={handleSubmit} className="">
                <div className="flex items-center justify-center flex-col">
                    <input
                        type="text"
                        className="outline-none rounded-md py-2 px-4 bg-zinc-700 placeholder:text-black my-2"
                        placeholder="Username"
                        autoComplete="off"
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        type="password"
                        className="outline-none rounded-md py-2 px-4 bg-zinc-700 placeholder:text-black my-2"
                        placeholder="Password"
                        autoComplete="off"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button
                    type="submit"
                    className="px-24 py-2 mt-10 rounded-md bg-white text-black"
                >
                    login
                </button>
            </form>
            {loading&&<div className="bg-[#00000070] fixed h-screen w-full animate-pulse"><p className="bg-white p-10 text-black">Loading</p></div>}
            {error?<div className="bg-[#00000070] fixed h-screen w-full"><p className="bg-white p-10 text-black">Error</p></div>:<div></div>}
        </div>
    );
}

export default Login;
