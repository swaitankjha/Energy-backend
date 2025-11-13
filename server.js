const express = require("express");
const app = express();
app.use(express.json());

let latestData = {};

app.post("/api/update", (req, res) => {
    latestData = req.body;
    console.log("ESP32 sent:", latestData);
    res.send({ status: "ok" });
});

app.get("/api/data", (req, res) => {
    res.send(latestData);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Server running on", PORT));
