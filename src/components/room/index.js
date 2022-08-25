
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './room.css'

import Chat from "../../components/chat/"
import Video from "../../components/video/"

function Room({ socket }) {
    const { state } = useLocation()
    const { username, room } = state

    const joinRoom = () => {

        const roomData = {
            name:username,
            room:room
        }

        if (username !== "" && room !== "") {
            socket.emit("join_room", roomData);

        }
    }
    useEffect(() => {
        if (socket.connected === false) {

            joinRoom();
        }
    }, [socket])

    return (
        <div className="room">
            <div className="container-fluid corpo-principal">
                <div className="row linha-principal">
                    <div className="col-lg-8 card-video">

                        <Video socket={socket} room={room} />
                    </div>
                    <div className="col-lg-4 card-chat">
                        <Chat socket={socket} username={username} room={room} /></div>
                </div>
            </div>

        </div>
    );
};

export default Room;