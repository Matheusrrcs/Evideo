import { useEffect, useState } from 'react';
import "./chat.css"
import ScrollToBottom from 'react-scroll-to-bottom'

function Chat({ socket, username, room }) {

    const [currentMessage, setCurrentMessage] = useState("");

    const [messageList, setMessageList] = useState([]);

    const sendMessage = async () => {
        // verifica se tem alguma message
        if (currentMessage !== "") {

            //estrutura da message 
            const messageData = {
                room: room,
                name: username,
                message: currentMessage,
                history: "",
                time: new Date(Date.now()).getHours() + ":" + new Date(Date.now()).getMinutes(),

            };
            // envia a message para o backend
            await socket.emit("send_message", messageData);
            setMessageList((list) => [...list, messageData]);

            setCurrentMessage("");
        }
    }

    useEffect(() => {
        //evento que pega as informações da mensagem do backend
        socket.on("receive_message", (data) => {
        
            setMessageList((list) => [...list, data])

        })

    }, [socket])

    return (
        <div className="chat">
            <div className="chat-header">
                <p className="but"><span className="bol"></span>Chat</p>
            </div>
            <div className="chat-body">
                <ScrollToBottom className='chat-body'>
                    {messageList.map((messageContent) => {
                        return <div className="message-body" id={username === messageContent.name ? "you" : "other"}>
                            <div className="user-img"><i className="fa-solid fa-user"></i></div>
                            <div className="message-content">
                                <div className="info-message">
                                    <small>{messageContent.name}</small>
                                    <small>{messageContent.time}</small>
                                </div>
                                <div className="msg">
                                    <p> {
                                        messageContent.message
                                    }</p>
                                </div>
                            </div>
                        </div>
                    })}
                </ScrollToBottom>
            </div>
            <div className="chat-footer">
                <form onSubmit={(e) => { e.preventDefault() }}>
                    <input type="text" value={currentMessage} placeholder='Digite uma mensagem' onChange={(e) => {
                        setCurrentMessage(e.target.value)

                    }} />
                    <button className="but" onClick={() => { sendMessage() }}>Enviar</button>


                </form>
            </div>

        </div>
    );
}

export default Chat;