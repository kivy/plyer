const net = require("net");

const VOIPserver = net.createServer((socket) => {
    let clientAddress = socket.remoteAddress;
    console.log(`Client connected: ${clientAddress}`);

    // When data is received, send it back to sender for testing
    socket.on("data", (data) => {
        socket.write(data);
    });
    socket.on("end", () => {
        console.log('Client disconnected');
    });
    socket.on("error", (err) => {});
});

const PORT = 8080;
VOIPserver.listen(PORT, () => {
  console.log(`VOIP server running on ${PORT}`);
});
