const express = require('express');
const app = express();
const http = require('http');
const cors = require('cors');
const { Server } = require('socket.io');
const { inflate } = require('zlib');
app.use(cors());




// cria o servidor
const server = http.createServer(app);


//configuração do socket.io
const io = new Server(server, {
    cors: {
        origin: "http://localhost:3000",
        methods: ["GET", "POST"],
    }
});



// evento do socket quando cliente for conectador
io.on("connection", (socket) => {
    // console.log(`Usuario Conectado": ${socket.id}`);

    // se conecta com a sala digitada 
    socket.on("join_room", (data) => {
        socket.join(data.room);

        console.log(`Usuario com a ID:${socket.id} se juntou a sala: ${data.room} `)
    })

    // envia os dados da mensagem recebida de volta para o front
    socket.on("send_message", (data) => {

        socket.to(data.room).emit("receive_message", data);
    })

    // envia os dado do video de volta para o front
    socket.on("send_video", (data) => {
        video = data;
        socket.to(data.room).emit("recive_video", data);
    })

    // envia os dados para da play no video
    socket.on("play_video", (data) => {
        data.play = true;
        socket.to(data.room).emit("recive_play", data);
    })
    // envia os dados para pausar o video
    socket.on("pause_video", (data) => {
        data.pause = false;
        socket.to(data.room).emit("recive_pause", data);
    })



    socket.on("progress_video", (data) => {
        console.log(data.progress)
        socket.to(data.room).emit("recive_progress", data);
    })


    socket.on("disconnect", () => {
        // console.log("Usuario desconectado", socket.id);
    })
})


const PORT = process.env.PORT || 3001;

//cria um listener
server.listen(PORT, () => {
    console.log("SERVIDOR RODANDO")
});