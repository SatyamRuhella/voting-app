const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Route to display the voting page
app.get('/', (req, res) => {
    res.render('index');
});

// Route to cast a vote
app.post('/castVote', async (req, res) => {
    try {
        const { party } = req.body;
        await axios.post('http://localhost:5000/vote', { party });
        res.send("Vote cast successfully!");
    } catch (error) {
        res.status(500).send("Error casting vote.");
    }
});

// Route to get the voting results
app.get('/results', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/results');
        res.render('results', { results: response.data });
    } catch (error) {
        res.status(500).send("Error fetching results.");
    }
});

app.listen(PORT, () => {
    console.log(`Frontend running on http://localhost:${PORT}`);
});

