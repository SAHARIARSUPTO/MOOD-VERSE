const express = require("express");
const { PythonShell } = require("python-shell");
const cors = require("cors");
const http = require("http");
const { Server } = require("socket.io");
const { MongoClient, ServerApiVersion } = require("mongodb");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
  },
});

const port = 5000;

app.use(cors());
app.use(express.json());

const uri =
  "mongodb+srv://moodverse:moodverse@cluster0.nyrjtse.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  },
});

let moodCollection;

async function connectDB() {
  try {
    await client.connect();
    const db = client.db("MoodVerseDB");
    moodCollection = db.collection("moods");
    console.log("✅ Connected to MongoDB");
  } catch (err) {
    console.error("❌ MongoDB connection error:", err);
  }
}

connectDB();

io.on("connection", (socket) => {
  console.log("✅ WebSocket client connected");

  socket.on("disconnect", () => {
    console.log("❌ WebSocket client disconnected");
  });

  socket.on("requestScan", () => {
    console.log("🔁 Client requested a new scan");
    // Optional: Hook in real-time scan trigger here
  });
});

app.post("/start-mood-detection", (req, res) => {
  const options = {
    mode: "text",
    pythonPath: "C:/Program Files/Python310/python.exe",
    scriptPath: "D:/MoodVerse-Py",
    args: [],
  };

  PythonShell.run("face_mood.py", options, (err, results) => {
    if (err) {
      console.error("Error running Python script:", err);
      res
        .status(500)
        .send({ error: "Error running Python script", details: err.message });
      return;
    }
    console.log("Python script results:", results);
    res.json({ mood: "happy", result: results });
  });
});

app.post("/mood-update", (req, res) => {
  const mood = req.body.mood;
  console.log(`Received mood: ${mood}`);
  io.emit("moodUpdate", { mood });
  res.status(200).send({ status: "success" });
});

app.post("/mood-track", async (req, res) => {
  const { name, age, mood, time } = req.body;
  try {
    const result = await moodCollection.insertOne({ name, age, mood, time });
    console.log("📝 Mood data stored:", result.insertedId);
    res.status(201).send({ success: true, id: result.insertedId });
  } catch (err) {
    console.error("❌ Failed to store mood data:", err);
    res.status(500).send({ success: false, error: err.message });
  }
});
app.get("/mood-history", async (req, res) => {
  const { name, age } = req.query;

  if (!name || !age) {
    return res.status(400).json({ error: "Name and age are required." });
  }

  try {
    const history = await moodCollection
      .find({ name, age })
      .sort({ time: 1 })
      .toArray();

    res.status(200).json(history);
  } catch (err) {
    console.error("❌ Failed to fetch mood history:", err);
    res.status(500).json({ error: "Failed to fetch mood history" });
  }
});

server.listen(port, () => {
  console.log(`🚀 Server running on http://localhost:${port}`);
});
