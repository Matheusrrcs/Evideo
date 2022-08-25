
import './configure.css';
import io from 'socket.io-client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';



function Configure({ socket }) {

    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [room, setRoom] = useState("");
    const [error, setError] = useState(false);

    // verficar se usario e a sala não estão vazios e envia o room pro backend
    const joinRoom = () => {

        if (username !== "" && room !== "") {

            const roomData = {
                name: username,
                room: room
            }

            socket.emit("join_room", roomData);

            setError(false);

            navigate("/room", { state: { username: username, room: room } })

        }
        else {
            setError(true);
            setTimeout(() => {
                setError(false);
            }, 2000);
        };
    }

    return (
        <div className="configure">

            <div className="title">
                <h3>Entrar na sala</h3>
            </div>
            <form className="form" onClick={(e) => e.preventDefault()}>
                <input type="text" placeholder="Usuario" onChange={(e) => { setUsername(e.target.value); }} />
                <input type="text" placeholder="ID da sala" onChange={(e) => { setRoom(e.target.value); }} />
                <button className="but" onClick={() => {
                    joinRoom()

                }}>Entrar</button>

            </form>

            {
                error && (
                    < div className="px-5 pt-3" >
                        <div className="alert alert-danger test -white text-center" role="alert" >
                            Preencha todos os campos
                        </div>
                    </div>
                )
            }
        </div>
    );
}

export default Configure;
