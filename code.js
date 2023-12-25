const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
 res.send('Welcome to the API!');
});

app.get('/users', (req, res) => {
 res.json([
    { id: 1, name: 'John' },
    { id: 2, name: 'Jane' },
 ]);
});

app.post('/users', (req, res) => {
 const newUser = {
    id: Date.now(),
    name: req.body.name,
 };

 res.status(201).json(newUser);
});

app.put('/users/:id', (req, res) => {
 res.json({
    id: req.params.id,
    name: req.body.name,
 });
});

app.delete('/users/:id', (req, res) => {
 res.send(`User with ID ${req.params.id} has been deleted.`);
});

app.listen(port, () => {
 console.log(`Server is running at http://localhost:${port}`);
});