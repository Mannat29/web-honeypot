const express = require("express");
const router = express.Router();
const auth = require("../middleware/auth");
const Task = require("../models/Task");

// GET /api/tasks
router.get("/", auth, async (req, res) => {
  const tasks = await Task.find({ userId: req.user });
  res.json(tasks);
});

// POST /api/tasks
router.post("/", auth, async (req, res) => {
  const { title } = req.body;

  const task = new Task({
    title,
    userId: req.user,
  });

  await task.save();
  res.json(task);
});

// PUT /api/tasks/:id
router.put("/:id", auth, async (req, res) => {
  const { completed } = req.body;

  const task = await Task.findOneAndUpdate(
    { _id: req.params.id, userId: req.user },
    { completed },
    { new: true }
  );

  if (!task) {
    return res.status(404).json({ message: "Task not found" });
  }

  res.json(task);
});

// DELETE /api/tasks/:id
router.delete("/:id", auth, async (req, res) => {
  const task = await Task.findOneAndDelete({
    _id: req.params.id,
    userId: req.user,
  });

  if (!task) {
    return res.status(404).json({ message: "Task not found" });
  }

  res.json({ message: "Task deleted" });
});

module.exports = router;
