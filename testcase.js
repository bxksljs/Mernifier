const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const MockAdapter = require('axios-mock-adapter');
const program = require('commander');
const app = require('./app');

// Generate test cases for each route
function generateTestCases(app) {
    const mock = new MockAdapter(axios);
    const routes = [
        { method: 'get', url: '/' },
        { method: 'post', url: '/' },
        { method: 'put', url: '/' },
        { method: 'delete', url: '/' },
    ];

    routes.forEach(route => {
        mock[route.method](route.url)
            .reply(200, { success: true });
    });

    // Execute the requests and generate test cases
    routes.forEach(route => {
        axios[route.method](`http://localhost:${port}${route.url}`)
            .then(response => {
                console.log(`${route.method.toUpperCase()} ${route.url} =>`, response.data);
            })
            .catch(error => {
                console.error(`${route.method.toUpperCase()} ${route.url} =>`, error);
            });
    });
}

// Set up command-line options and start the server
program
    .version('1.0.0')
    .option('-c, --code <code>', 'The path to the code to be tested')
    .parse(process.argv);

if (program.code) {
    const userCode = require(program.code);
    const app = userCode.app;
    const port = userCode.port || 3000;

    app.listen(port, () => {
        console.log(`Server is running on port ${port}`);
        generateTestCases(app);
    });
} else {
    program.help();
}