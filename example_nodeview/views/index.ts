import {createSocket, Socket} from "zeromq";

interface ServerMessage {
    view: string;
    data: any;
}

interface IntoJSON {
    toJSON(): object;
}

createServer("tcp://*:5000", msg =>
    `<h1>View: ${msg.view}</h1><p><pre><code>${JSON.stringify(msg.data)}</code></pre></p>`)
    .then(kill => {
        console.log("Server started");
        process.on("beforeExit", () => {
            console.log("Killing server");
            kill();
        });
    })
    .catch(err => {
        console.log("Critical error: ", err);
        process.exit(1);
    })

function createServer(addr: string, onMessage: (msg: ServerMessage) => string | IntoJSON): Promise<() => void> {
    const sock = createSocket("rep");
    return new Promise((resolve, reject) => {
        sock.bind(addr, err => {
            if (err) reject(err);
            resolve();
        });
    }).then(() => {
        sock.on("message", msg => {
            let response: string | IntoJSON;
            console.log("[DEBUG] Message:", msg);
            if (msg instanceof Buffer) {
                const strMessage = msg.toString("utf-8");
                console.log("[DEBUG] Message: ", strMessage);
                response = onMessage(JSON.parse(strMessage));
            }
            else if (typeof msg === "string") response = onMessage(JSON.parse(msg));
            else {
                console.warn("Multipart messages not yet supported");
                sock.send(JSON.stringify({error: "Multipart message not yet supported"}));
                return;
            }
            if (typeof response === "string") {
                sock.send(response);
            } else {
                sock.send(JSON.stringify(response.toJSON()));
            }
        });
        return Socket.prototype.close.bind(sock);
    })
}