
import "./video.css"
import ReactPlayer from 'react-player'
import { useEffect, useState } from "react";

function Video({ socket, room }) {

    const [linkVideo, setLinkVideo] = useState("");
    const [link, setLink] = useState("");

    const [dnone, setDnone] = useState("");

    const [progressVideo, setProgressVideo] = useState("");
    const [finishVideo, setFinishVideo] = useState("");

    const [playPause, setPlayPause] = useState(false);

    const sendVideo = async () => {
        // verifica se tem alguma message

        if (linkVideo !== "") {

            setDnone("d-none")
            //estrutura da message 
            const videoData = {
                room: room,
                link: linkVideo,
                name: "matheus"

            };
            setLink(videoData.link)
            setLinkVideo("")
            await socket.emit("send_video", videoData);

        }
    }

    const playVideo = async () => {


        const playPauseData = {
            room: room,
            play: playPause
        };
        setPlayPause(true);
        await socket.emit("play_video", playPauseData);

    }

    const pauseVideo = async () => {


        const pauseData = {
            room: room,
            pause: playPause
        };
        setPlayPause(false);
        await socket.emit("pause_video", pauseData);

    }
    const progress = async (state) => {

        const progressData = {
            room: room,
            progress: progressVideo
        };
        setProgressVideo(state.playedSeconds)
        await socket.emit("progress_video", progressData);


    }

    useEffect(() => {

        //evento que pega as informações da mensagem do backend
        socket.on("recive_video", (data) => {
            setDnone("d-none")
            setLink(data.link)

        })

        socket.on("recive_pause", (data) => {
            setPlayPause(data.pause)

        })

        socket.on("recive_play", (data) => {
            setPlayPause(data.play)

        })

        socket.on("recive_progress", (data) => {
            setProgressVideo(data.progress)


        })

    }, [socket])

    return (

        <div className="video">

            <div className={`link-btn ${dnone}`}>
                <div className="icone-video">
                    <i class="fa-solid fa-link"></i>
                </div>

                <div className="title pb-4">
                    <h2>Procurar video</h2>
                </div>

                <form className="video-form">
                    <input type="text" placeholder="Link do video" value={linkVideo} onChange={(e) => setLinkVideo(e.target.value)} />
                    <button type="button" className="but" onClick={() => {

                        sendVideo();


                    }}>Pesquisar</button>
                </form>



            </div>

            {
                link !== "" ?

                    <ReactPlayer url={link} width="90%" height="90%" controls={true} playing={playPause} clasName={finishVideo}
                        onStart={() => { playVideo() }}
                        onPlay={() => { playVideo() }}
                        onProgress={progress}
                        onEnded={() => {
                            setDnone("")
                            setLink("")
                        }}
                        onPause={() => { pauseVideo() }}
                    />
                    :
                    ""


            }
        </div>

    );

}

export default Video;