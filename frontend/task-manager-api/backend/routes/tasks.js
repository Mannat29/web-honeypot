const express = require("express");
const router = express.Router();
const auth = require("../middleware/auth");

const Task = require("../models/Task");

// Get tasks
router.get("/", auth, async (req, res) => {
    const tasks = await Task.find({ userId: req.user });
    res.json(tasks);
});

// Add task
router.post("/", auth, async (req, res) => {
    const { title } = req.body;

    const task = new Task({
        title,
        userId: req.user
    });

    await task.save();
    res.json(task);
});

// Update task
router.put("/:id", auth, async (req, res) => {
    const { completed } = req.body;

    const task = await Task.findOneAndUpdate(
        { _id: req.params.id, userId: req.user },
        { completed },
        { new: true }
    );

    res.json(task);
});

// Delete task
router.delete("/:id", auth, async (req, res) => {
    await Task.findOneAndDelete({ _id: req.params.id, userId: req.user });
    res.json({ message: "Task deleted" });
});

module.exports = router;
