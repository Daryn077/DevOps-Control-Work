const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Hello World' });
});

app.get('/api/info', (req, res) => {
  res.json({
    framework: "Express.js",
    language: "JavaScript",
    docker: true
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: "ok"
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server listening on port ${PORT}`);
});
