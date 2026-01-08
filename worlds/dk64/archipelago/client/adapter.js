var server = new Server();
var port = 0;
// Read pj64.installDirectory
var install_directory = pj64.installDirectory;
// Read install_dir/Config/Project64.cfg, it already exists
var config_path = install_directory + "Config\\Project64.cfg";
console.log("Config path: " + config_path);
var file = fs.readfile(config_path.toString()).toString();
// Find the line that starts with "AP_PORT=" and get the port number
var lines = file.split("\n");
for (var i = 0; i < lines.length; i++) {
    if (lines[i].startsWith("ap_port=")) {
        var portLine = lines[i].split("=")[1].trim();
        port = parseInt(portLine, 10);
        if (isNaN(port)) {
            console.log("Invalid port number in Project64.cfg: " + portLine);
            port = 48080; // Default to 0 if invalid
        } else {
            console.log("Port number found in Project64.cfg: " + port);
        }
        break;
    }
}

var ip = "127.0.0.1";
function startServer() {
    console.log("Starting server...");
    server.listen(port, ip);

    server.on('connection', function(c) {
        console.log("Client connected");

        // Flag to track if the connection is alive
        var isConnected = true;

        c.on('data', function(data) {
            if (!isConnected) return;

            var message = data.toString().trim();
            var parts = message.split(':');
            if (parts.length < 2) {
                c.write("Invalid message format\n");
                return;
            }

            var messageId = parts[0];
            var command = parts.slice(1).join(':').trim();

            if (command.startsWith("read")) {
                var readParts = command.split(" ");
                if (readParts.length === 4) {
                    var type = readParts[1];
                    var address = parseInt(readParts[2], 16);
                    var size = parseInt(readParts[3], 10);
                    if (!isNaN(address) && !isNaN(size) && size > 0) {
                        var result = [];
                        if (type === "bytestring") {
                            for (var i = 0; i < size; i++) {
                                result.push(String.fromCharCode(mem.u8[address + i]));
                            }
                            c.write(messageId + ":" + result.join("") + "\n");
                            return;
                        }
                        else if (type === "u8") {
                            for (var i = 0; i < size; i++) {
                                result.push(mem.u8[address + i]);
                            }
                        } else if (type === "u16") {
                            for (var i = 0; i < size; i += 2) {
                                result.push(mem.u16[address + i]);
                            }
                        } else if (type === "u32") {
                            for (var i = 0; i < size; i += 4) {
                                result.push(mem.u32[address + i]);
                            }
                        } else {
                            c.write(messageId + ":Invalid type, use: read u8, read u16, read u32\n");
                            return;
                        }
                        c.write(messageId + ":" + result.join("") + "\n");
                    } else {
                        c.write(messageId + ":Invalid read parameters\n");
                    }
                } else {
                    c.write(messageId + ":Usage: read u8/u16/u32 0xADDRESS SIZE\n");
                }
            }
            else if (command.startsWith("dict")) {
                // Remove "dict " from the beginning
                var dict = command.substring(5);
                try {
                    dict = JSON.parse(dict);
                } catch (e) {
                    console.log(e)
                    c.write(messageId + ":Invalid JSON format for dictionary\n");
                    return;
                }
                // eg dict {"name": {"type": "u8", "adr": 0x1234, "size": 4}}
                var result = {};
                for (var key in dict) {
                    var item = dict[key];
                    // If the item is not a dict, assume we just got the address and convert it to a dict
                    if (typeof item !== "object") {
                        item = {"adr": item};
                    }
                    // If type is not defined default to u8
                    if (!item.type) {
                        item.type = "u8";
                    }
                    if (!item.size) {
                        item.size = 1;
                    }
                    if (item.type === "u8") {
                        var values = [];
                        for (var i = 0; i < item.size; i++) {
                            values.push(mem.u8[item.adr + i]);
                        }
                        result[key] = values;
                    } else if (item.type === "u16") {
                        var values = [];
                        for (var i = 0; i < item.size; i += 2) {
                            values.push(mem.u16[item.adr + i]);
                        }
                        result[key] = values;
                    } else if (item.type === "u32") {
                        var values = [];
                        for (var i = 0; i < item.size; i += 4) {
                            values.push(mem.u32[item.adr + i]);
                        }
                        result[key] = values;
                    } else {
                        c.write(messageId + ":Invalid type, use: u8, u16, u32\n");
                        return;
                    }
                }
                c.write(messageId + ":" + JSON.stringify(result) + "\n");
                return;
            }
            else if (command.startsWith("write")) {
                var writeParts = command.split(" ");
                var type = writeParts[1];
                var address = parseInt(writeParts[2], 16);
                var value = writeParts.slice(3).join(" ");
                if (type === "bytestring") {
                    var byteArray = [];

                    for (var i = 0; i < value.length; i++) {
                        byteArray.push(value.charCodeAt(i));
                    }
                    for (var i = 0; i < byteArray.length; i++) {
                        mem.u8[address + i] = byteArray[i];
                    }
                    c.write(messageId + ":Bytestring write successful\n");
                    return;
                }
        
                try {
                    value = JSON.parse(value);
                } catch (e) {
                    c.write(messageId + ":Invalid JSON format for value\n");
                    return;
                }
        
                if (!Array.isArray(value)) {
                    c.write(messageId + ":Value must be an array\n");
                    return;
                }
        
                if (!isNaN(address) && !isNaN(value)) {
                    if (type === "u8") {
                        for (var i = 0; i < value.length; i++) {
                            mem.u8[address + i] = value[i];
                        }
                    } else if (type === "u16") {
                        for (var i = 0; i < value.length; i += 2) {
                            mem.u16[address + i] = value[i / 2];
                        }
                    } else if (type === "u32") {
                        for (var i = 0; i < value.length; i += 4) {
                            mem.u32[address + i] = value[i / 4];
                        }
                    } else {
                        c.write(messageId + ":Invalid type, use: write u8, write u16, write u32, write bytestring\n");
                        return;
                    }
                    c.write(messageId + ":Write successful\n");
                } else {
                    c.write(messageId + ":Invalid write parameters\n");
                }
            }
            else if (command === "romInfo"){
                c.write(messageId + ":" + JSON.stringify(pj64.romInfo) + "\n");
            } else {
                c.write(messageId + ":Unknown command\n");
            }
        });

        c.on('end', function() {
            console.log("Client ended connection");
            isConnected = false;
        });

        c.on('close', function() {
            console.log("Client disconnected unexpectedly");
            isConnected = false;
        });

        c.on('error', function(err) {
            if (isConnected === false) return;
            console.log("Connection error: " + err.message);
            isConnected = false;
            c.close();
            restartServer();
        });
    });


    console.log("Server attempting to listen on " + ip + ":" + port);
    // Check if the server is actually listening
    server.on('listening', function() {
        console.log("Server is listening on " + ip + ":" + port);
    });

    server.on('error', function(err) {
        console.log("Server failed to start: " + err.message);
        // If its a bind error raise an alert
        if (err.message.includes("(10013)")) {
            console.log("Port " + port + " is already in use. Please close the other application or change the port.");
            alert("Port " + port + " is already in use. Please close the duplicate PJ64 or change the port in your PJ64 config file.");
        } else {
            console.log("Server error: " + err.message);
        }
    });
}

function restartServer() {
    console.log("Restarting server...");
    server.close()
    server = new Server();
    setTimeout(startServer, 5000);
}

startServer();
