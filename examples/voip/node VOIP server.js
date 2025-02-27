const net = require("net");

const VOIPserver = net.createServer((socket) => {
    let clientAddress = socket.remoteAddress;
    console.log(`Client connected: ${clientAddress}`);

    // When data is received, send it back to sender for testing
    socket.on("data", (data) => {
        socket.write(data);
    });
    /*
    Socket.on(end) will not catch socket closure
    due to javascript and java handling sockets differrently,
    causing an error.
    */
    socket.on("error", (err) => {
        console.log(`Client disconnected: ${clientAddress}`);
    });
});

const PORT = 8080;
VOIPserver.listen(PORT, () => {
  console.log(`VOIP server running on ${PORT}`);
});
