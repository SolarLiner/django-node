import {createSocket} from "zeromq";

async function createZeroServer(addr: string, cb: (msg: string) => string): Promise<void> {
    const sock = createSocket("rep");
    return new Promise(((resolve, reject) => {
        sock.bind(addr, err => {
            if (err) reject(err);
            resolve();
        });
    })).then(() => {
        console.log("Server ready");
        sock.on("message", msg => {
            if(msg instanceof Buffer) sock.send(cb(msg.toString("utf-8")))
            else if(msg instanceof Array) sock.send(msg.map(v => v.toString()).map(cb));
            else sock.send(cb(msg));
        });
    });
}

createZeroServer("tcp://*:5000", msg => msg.anchor("anchor-name"))
    .catch(err => {
        console.error("Error bringing server up", err);
        process.exit(1);
    });