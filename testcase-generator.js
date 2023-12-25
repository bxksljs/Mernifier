const fs = require('fs');
const express = require('express');
const chai = require('chai');
const chaiHttp = require('chai-http');
const chaiThings = require('chai-things');
const mkdirp = require('mkdirp');
const path = require('path');

chai.use(chaiHttp);
chai.use(chaiThings);

function generateTestCases(codeFile, callback) {
    const app = express();
    const testCaseFolder = 'test-cases';
    mkdirp.sync(testCaseFolder);

    // Add your routes here
    app.get('/test', (req, res) => {
        res.send('GET request received');
    });

    app.post('/test', (req, res) => {
        res.send('POST request received');
    });

    app.put('/test', (req, res) => {
        res.send('PUT request received');
    });

    app.delete('/test', (req, res) => {
        res.send('DELETE request received');
    });

    // Add your request parameters and assertions here
    const testCases = [];
    ['get', 'post', 'put', 'delete'].forEach(method => {
        testCases.push({
            method: method,
            url: '/test',
            assertions: [
                { key: 'body', value: `${method.toUpperCase()} request received` },
                { key: 'status', value: 200 },
            ],
        });
    });

    // Generate the test cases and save them in a file
    let testCaseFileContent = 'const chai = require("chai");\n';
    testCaseFileContent += 'const chaiHttp = require("chai-http");\n';
    testCaseFileContent += 'const server = require("../index");\n';
    testCaseFileContent += 'chai.use(chaiHttp);\n';
    testCaseFileContent += 'describe("API tests", () => {\n';

    testCases.forEach((testCase, index) => {
        testCaseFileContent += ` it("should handle ${testCase.method.toUpperCase()} request on ${testCase.url}", (done) => {\n`;
        testCaseFileContent += `    chai.request(server)\n`;
        testCaseFileContent += `      .${testCase.method}(${JSON.stringify(testCase.url)})\n`;
        testCaseFileContent += `      .end((err, res) => {\n`;

        testCase.assertions.forEach((assertion) => {
            testCaseFileContent += `        chai.expect(res).to.have.${assertion.key}(${JSON.stringify(assertion.value)});\n`;
        });

        testCaseFileContent += '        done();\n';
        testCaseFileContent += '      });\n';
        testCaseFileContent += ' });\n';
    });

    testCaseFileContent += '});\n';

    const testCaseFileName = `test-case-${Date.now()}.js`;
    const testCaseFilePath = path.join(testCaseFolder, testCaseFileName);
    fs.writeFileSync(testCaseFilePath, testCaseFileContent);

    callback(null, testCaseFilePath);
}

module.exports = generateTestCases;
